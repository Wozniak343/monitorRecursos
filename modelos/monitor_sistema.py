from __future__ import annotations
import json
import platform
import re
import shutil
import subprocess
import time
from typing import Any
import psutil

class MonitorSistema:
    MAX_PROCESOS_MOSTRADOS = 50

    def __init__(self) -> None:
        self._ruta_nvidia_smi = shutil.which("nvidia-smi")
        self._nombre_cpu = self._obtener_nombre_cpu()
        self._nombre_gpu = self._obtener_nombre_gpu()
        self._nombre_interfaz_red = self._obtener_nombre_interfaz_red()
        self._discos_cache: list[dict[str, Any]] = []
        self._ultimo_tiempo_discos = 0.0
        self._procesos_cache: list[dict[str, Any]] = []
        self._ultimo_tiempo_procesos = 0.0
        self._gpu_cache: dict[str, float] | None = None
        self._ultimo_tiempo_gpu = 0.0
        self._ultimo_registro_red = psutil.net_io_counters()
        self._ultimo_momento_red = time.perf_counter()
        self._precalentar_cpu_procesos()

    def obtener_resumen_sistema(self) -> dict[str, Any]:
        memoria = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=None)
        red = self._obtener_uso_red()
        discos = self.obtener_dispositivos_disco()
        gpu = self._obtener_info_gpu()

        return {
            "cpu_porcentaje": cpu,
            "cpu_nombre": self._nombre_cpu,
            "memoria_porcentaje": memoria.percent,
            "memoria_usada_gb": memoria.used / (1024**3),
            "memoria_total_gb": memoria.total / (1024**3),
            "disco_principal_porcentaje": discos[0]["porcentaje"] if discos else 0.0,
            "disco_principal_usado_gb": discos[0]["usado_gb"] if discos else 0.0,
            "disco_principal_total_gb": discos[0]["total_gb"] if discos else 0.0,
            "discos": discos,
            "red_subida_kbps": red["subida_kbps"],
            "red_bajada_kbps": red["bajada_kbps"],
            "nombre_interfaz_red": self._nombre_interfaz_red,
            "gpu_porcentaje": gpu["utilizacion_porcentaje"],
            "gpu_temperatura_c": gpu["temperatura_c"],
            "gpu_memoria_usada_mb": gpu["memoria_usada_mb"],
            "gpu_memoria_total_mb": gpu["memoria_total_mb"],
            "gpu_nombre": self._nombre_gpu,
            "cantidad_procesos": len(psutil.pids()),
        }

    def obtener_procesos_mas_pesados(self, cantidad: int = 50) -> list[dict[str, Any]]:
        cantidad = max(1, min(cantidad, self.MAX_PROCESOS_MOSTRADOS))
        tiempo_actual = time.perf_counter()
        if self._procesos_cache and (tiempo_actual - self._ultimo_tiempo_procesos) < 2.0:
            return self._procesos_cache[:cantidad]

        procesos: list[dict[str, Any]] = []

        for proceso in psutil.process_iter(["pid", "name", "memory_info", "memory_percent"]):
            try:
                memoria_info = proceso.info.get("memory_info")
                procesos.append(
                    {
                        "pid": proceso.info.get("pid", 0),
                        "nombre": proceso.info.get("name") or "Proceso desconocido",
                        "cpu_porcentaje": float(proceso.cpu_percent(None)),
                        "memoria_mb": (memoria_info.rss / (1024**2)) if memoria_info else 0.0,
                        "memoria_porcentaje": proceso.info.get("memory_percent", 0.0) or 0.0,
                    }
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        procesos.sort(key=lambda elemento: (elemento["cpu_porcentaje"], elemento["memoria_porcentaje"]), reverse=True)
        self._procesos_cache = procesos
        self._ultimo_tiempo_procesos = tiempo_actual
        return procesos[:cantidad]

    def obtener_dispositivos_disco(self) -> list[dict[str, Any]]:
        tiempo_actual = time.perf_counter()
        if self._discos_cache and (tiempo_actual - self._ultimo_tiempo_discos) < 5.0:
            return self._discos_cache

        discos: list[dict[str, Any]] = []
        particiones = psutil.disk_partitions(all=False)

        for particion in particiones:
            try:
                uso = psutil.disk_usage(particion.mountpoint)
            except (psutil.NoSuchProcess, psutil.PermissionError, OSError):
                continue

            discos.append(
                {
                    "dispositivo": particion.device,
                    "punto_montaje": particion.mountpoint,
                    "tipo": particion.fstype or "N/D",
                    "porcentaje": uso.percent,
                    "usado_gb": uso.used / (1024**3),
                    "total_gb": uso.total / (1024**3),
                }
            )

        discos.sort(key=lambda elemento: elemento["porcentaje"], reverse=True)
        self._discos_cache = discos
        self._ultimo_tiempo_discos = tiempo_actual
        return discos

    def finalizar_proceso(self, pid: int) -> None:
        proceso = psutil.Process(pid)
        proceso.terminate()
        try:
            proceso.wait(timeout=3)
        except (psutil.TimeoutExpired, psutil.NoSuchProcess):
            try:
                proceso.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def _obtener_uso_red(self) -> dict[str, float]:
        momento_actual = time.perf_counter()
        contador_actual = psutil.net_io_counters()

        intervalo = max(momento_actual - self._ultimo_momento_red, 1e-6)
        bytes_subida = contador_actual.bytes_sent - self._ultimo_registro_red.bytes_sent
        bytes_bajada = contador_actual.bytes_recv - self._ultimo_registro_red.bytes_recv

        self._ultimo_registro_red = contador_actual
        self._ultimo_momento_red = momento_actual

        return {
            "subida_kbps": (bytes_subida / intervalo) / 1024,
            "bajada_kbps": (bytes_bajada / intervalo) / 1024,
        }

    def _obtener_info_gpu(self) -> dict[str, float]:
        tiempo_actual = time.perf_counter()
        if self._gpu_cache is not None and (tiempo_actual - self._ultimo_tiempo_gpu) < 3.0:
            return self._gpu_cache

        if not self._ruta_nvidia_smi:
            self._gpu_cache = self._obtener_info_gpu_generica()
            self._ultimo_tiempo_gpu = tiempo_actual
            return self._gpu_cache

        try:
            comando = [
                self._ruta_nvidia_smi,
                "--query-gpu=name,utilization.gpu,temperature.gpu,memory.used,memory.total",
                "--format=csv,noheader,nounits",
            ]
            resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
            lineas = [l.strip() for l in resultado.stdout.strip().splitlines() if l.strip()]
            nombres: list[str] = []
            utils: list[float] = []
            temps: list[float] = []
            mem_usada: list[float] = []
            mem_total: list[float] = []

            for linea in lineas:
                partes = [valor.strip() for valor in linea.split(",")]
                if len(partes) >= 5:
                    nombre = partes[0]
                    try:
                        util = float(partes[1])
                    except ValueError:
                        util = 0.0
                    try:
                        temp = float(partes[2])
                    except ValueError:
                        temp = 0.0
                    try:
                        musada = float(partes[3])
                    except ValueError:
                        musada = 0.0
                    try:
                        mtotal = float(partes[4])
                    except ValueError:
                        mtotal = 0.0

                    nombres.append(re.sub(r"\s+", " ", nombre))
                    utils.append(util)
                    temps.append(temp)
                    mem_usada.append(musada)
                    mem_total.append(mtotal)

            if nombres:
                nombre_combinado = " | ".join(nombres)
                util_prom = sum(utils) / len(utils) if utils else 0.0
                temp_max = max(temps) if temps else 0.0
                memoria_usada_sum = sum(mem_usada) if mem_usada else 0.0
                memoria_total_sum = sum(mem_total) if mem_total else 0.0

                self._gpu_cache = {
                    "nombre": nombre_combinado,
                    "utilizacion_porcentaje": float(util_prom),
                    "temperatura_c": float(temp_max),
                    "memoria_usada_mb": float(memoria_usada_sum),
                    "memoria_total_mb": float(memoria_total_sum),
                }
            else:
                raise ValueError("No se obtuvo información válida de nvidia-smi")
        except (subprocess.SubprocessError, ValueError, IndexError):
            self._gpu_cache = self._gpu_cache or {
                "nombre": self._nombre_gpu,
                "utilizacion_porcentaje": 0.0,
                "temperatura_c": 0.0,
                "memoria_usada_mb": 0.0,
                "memoria_total_mb": 0.0,
            }

        self._ultimo_tiempo_gpu = tiempo_actual
        return self._gpu_cache

    def _obtener_info_gpu_generica(self) -> dict[str, float]:
        nombre = self._nombre_gpu
        memoria_total_mb = 0.0

        if nombre == "GPU desconocida":
            nombre = self._obtener_nombre_gpu_generico()
        # Normalizar nombre si es GPU integrada
        if self._es_gpu_integrada(nombre):
            nombre = "Gráficos integrados"

        return {
            "nombre": nombre,
            "utilizacion_porcentaje": 0.0,
            "temperatura_c": 0.0,
            "memoria_usada_mb": 0.0,
            "memoria_total_mb": memoria_total_mb,
        }

    def _precalentar_cpu_procesos(self) -> None:
        for proceso in psutil.process_iter():
            try:
                proceso.cpu_percent(None)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    def _obtener_nombre_gpu(self) -> str:
        if not self._ruta_nvidia_smi:
            return self._obtener_nombre_gpu_generico()

        try:
            resultado = subprocess.run(
                [self._ruta_nvidia_smi, "--query-gpu=name", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                check=True,
            )
            nombre = resultado.stdout.strip().splitlines()[0].strip()
            if nombre:
                return re.sub(r"\s+", " ", nombre)
        except (subprocess.SubprocessError, IndexError):
            pass

        return "GPU desconocida"

    def _obtener_nombre_gpu_generico(self) -> str:
        # Intentar detectar GPUs en sistemas Unix/Linux usando lspci
        try:
            resultado = subprocess.run(["lspci", "-nnk"], capture_output=True, text=True, check=True)
            salida = resultado.stdout or ""
            nombres: list[str] = []
            for linea in salida.splitlines():
                if re.search(r"VGA|3D controller", linea, re.I):
                    # Después de ': ' suele venir la descripción del dispositivo
                    partes = linea.split(":", 1)
                    if len(partes) > 1:
                        nombre = partes[1].strip()
                        if nombre:
                            nombres.append(re.sub(r"\s+", " ", nombre))
            if nombres:
                nombre_unido = " | ".join(nombres)
                if self._es_gpu_integrada(nombre_unido):
                    return "Gráficos integrados"
                return nombre_unido
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

        # Último recurso: intentar comandos gráficos o devolver desconocida
        try:
            resultado = shutil.which("glxinfo")
            if resultado:
                out = subprocess.run([resultado, "-B"], capture_output=True, text=True, check=True).stdout
                for linea in out.splitlines():
                    if linea.lower().startswith("device:") or linea.lower().startswith("vendor:"):
                        nombre = linea.split(":", 1)[1].strip()
                        if nombre:
                            if self._es_gpu_integrada(nombre):
                                return "Gráficos integrados"
                            return re.sub(r"\s+", " ", nombre)
        except Exception:
            pass

        return "GPU desconocida"

    def _es_gpu_integrada(self, nombre: str) -> bool:
        if not nombre:
            return False
        clave = nombre.lower()
        integrada_indicadores = [
            "intel",
            "uhd",
            "iris",
            "hd graphics",
            "integrated",
            "radeon graphics",
            "radeon vega",
            "mendocino",
            "radeon 610",
            "radeon 610m",
            "radeon 620",
            "radeon rx vega",
        ]
        discreta_excluir = ["nvidia", "geforce", "gtx", "rtx", "quadro"]

        if any(term in clave for term in discreta_excluir):
            return False

        return any(term in clave for term in integrada_indicadores)

    def _obtener_nombre_cpu(self) -> str:
        # Intentar leer /proc/cpuinfo en sistemas tipo Unix
        try:
            with open("/proc/cpuinfo", "r", encoding="utf-8", errors="ignore") as f:
                for linea in f:
                    if linea.lower().startswith("model name") or linea.lower().startswith("cpu model"):
                        partes = linea.split(":", 1)
                        if len(partes) > 1:
                            nombre = partes[1].strip()
                            if nombre:
                                return re.sub(r"\s+", " ", nombre)
        except Exception:
            pass

        # Fallback a platform
        nombre = platform.processor().strip()
        if nombre:
            return re.sub(r"\s+", " ", nombre)

        return "CPU desconocida"

    def _obtener_nombre_interfaz_red(self) -> str:
        for interfaz, direcciones in psutil.net_if_addrs().items():
            if interfaz.lower() != "lo" and direcciones:
                return interfaz
        return "Ethernet"