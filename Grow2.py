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

hora_on = None
hora_off = None
pin_wifi_ok = machine.Pin(2, machine.Pin.OUT, machine.Pin.PULL_DOWN)

def main():
    global hora_on, hora_off

    print("Iniciando WiFi...")
    wlan = wifimgr.get_connection()
    if wlan is None:
        print("No se pudo conectar a la red WiFi.")
        while True:
            pass

    pin_wifi_ok.value(1)
    time.sleep(1)  # Espera breve para evitar conflicto de puertos

    ntptime.settime()
    hora_on, hora_off = cargar_config()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 80))
    sock.listen(5)
    print("Servidor escuchando en puerto 80")

    try:
        while True:
            temperatura, humedad = leer_sensor()
            temperatura = round(temperatura, 1)
            humedad = round(humedad, 1)

            ahora = hora_actual_segundos()

            if hora_on is not None and hora_off is not None:
                if hora_on < hora_off:
                    encender = hora_on <= ahora < hora_off
                else:
                    encender = ahora >= hora_on or ahora < hora_off
                pin_wifi_ok.value(1 if encender else 0)

            conn, addr = sock.accept()
            hora_on, hora_off = manejar_peticion(conn, addr, temperatura, humedad, hora_on, hora_off)

    except Exception as e:
        print("Error general:", e)

    finally:
        sock.close()
        print("Socket cerrado correctamente")

main()
