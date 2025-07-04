import machine
import socket
import wifimgr
import ujson
import time
import ntptime
from utils import (
    hora_a_segundos,
    hora_actual_segundos,
    guardar_config,
    cargar_config,
    leer_sensor,
    pagina_guev,
    manejar_peticion
)

# Pines
pin_wifi_ok = machine.Pin(2, machine.Pin.OUT, machine.Pin.PULL_DOWN)
gpio0 = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)  # Modo flashing si está bajo

# Variables globales de configuración
hora_on = None
hora_off = None
nombre = "GrowBox"

def controlar_rele(ahora, hora_on, hora_off):
    """
    Controla el pin de salida según la hora actual y configuración.
    """
    if hora_on is not None and hora_off is not None:
        if hora_on < hora_off:
            encender = hora_on <= ahora < hora_off
        else:
            encender = ahora >= hora_on or ahora < hora_off
        pin_wifi_ok.value(1 if encender else 0)

def iniciar_servidor():
    """
    Inicializa WiFi, servidor web y escucha las conexiones.
    """
    global hora_on, hora_off

    print("Iniciando WiFi...")
    wlan = wifimgr.get_connection()
    if wlan is None:
        print("No se pudo conectar a la red WiFi.")
        while True:
            pass  # Se queda en loop esperando intervención

    pin_wifi_ok.value(1)  # LED o relé test al inicio
    time.sleep(1)

    print("Sincronizando hora con NTP...")
    try:
        ntptime.settime()
    except Exception as e:
        print("Error sincronizando NTP:", e)

    hora_on, hora_off, nombre = cargar_config()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 80))
    sock.listen(5)
    print("Servidor escuchando en puerto 80")

    try:
        while True:
            temperatura, humedad = leer_sensor()

            # Redondeamos valores si no son None
            temperatura = round(temperatura, 1) if temperatura is not None else "--"
            humedad = round(humedad, 1) if humedad is not None else "--"

            ahora = hora_actual_segundos()
            controlar_rele(ahora, hora_on, hora_off)

            conn, addr = sock.accept()
            hora_on, hora_off, nombre = manejar_peticion(
            conn, addr, temperatura, humedad, hora_on, hora_off, nombre
            )

    except Exception as e:
        print("Error general:", e)

    finally:
        sock.close()
        print("Socket cerrado correctamente")

# Ejecutar programa
iniciar_servidor()
