import time
import ujson
import ahtx0
import machine
from machine import I2C, Pin
from guev import pagina_guev

# Inicialización I2C y sensor
i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000)
sensor = ahtx0.AHT10(i2c)
pin_wifi_ok = machine.Pin(2, machine.Pin.OUT, machine.Pin.PULL_DOWN)

def hora_a_segundos(hora_str):
    try:
        h, m = map(int, hora_str.split(":"))
        return h * 3600 + m * 60
    except:
        return None

def hora_actual_segundos():
    t = time.localtime(time.time() - 3 * 3600)  # UTC-3
    return t[3] * 3600 + t[4] * 60

def guardar_config(hora_on, hora_off, nombre):
    config = {
        "hora_on": hora_on,
        "hora_off": hora_off,
        "nombre": nombre
    }
    with open("config.json", "w") as f:
        ujson.dump(config, f)

def cargar_config():
    try:
        with open("config.json", "r") as f:
            config = ujson.load(f)
            hora_on = config.get("hora_on")
            hora_off = config.get("hora_off")
            nombre = config.get("nombre", "GrowBox")
            print("Configuración cargada:", hora_on, hora_off, nombre)
            return hora_on, hora_off, nombre
    except:
        print("No se encontró configuración previa.")
        return None, None, "GrowBox"

def enviar_respuesta(conn, tipo, contenido, codigo="200 OK"):
    conn.send("HTTP/1.1 {}\r\n".format(codigo))
    headers = {
        "json": "Content-Type: application/json\r\n",
        "html": "Content-Type: text/html\r\n",
        "text": "Content-Type: text/plain\r\n"
    }
    conn.send(headers.get(tipo, "") + "Connection: close\r\n\r\n")
    if tipo == "json":
        conn.sendall(ujson.dumps(contenido))
    elif tipo == "html":
        conn.sendall(contenido)
    elif tipo == "text":
        conn.sendall(contenido if isinstance(contenido, str) else str(contenido))
    else:
        conn.send("Error")

def manejar_peticion(conn, addr, temperatura, humedad, hora_on, hora_off, nombre):
    try:
        request = conn.recv(1024)
        request_str = request.decode()

        if 'POST /horas' in request_str:
            cuerpo = request_str.split("\r\n\r\n", 1)[1]
            datos = ujson.loads(cuerpo)

            nueva_on = hora_a_segundos(datos.get("encender", ""))
            nueva_off = hora_a_segundos(datos.get("apagar", ""))
            nuevo_nombre = datos.get("nombre", nombre)

            if (nueva_on is not None and 0 <= nueva_on < 86400 and
                nueva_off is not None and 0 <= nueva_off < 86400):
                guardar_config(nueva_on, nueva_off, nuevo_nombre)
                enviar_respuesta(conn, "text", "OK")
                return nueva_on, nueva_off, nuevo_nombre
            else:
                enviar_respuesta(conn, "text", "Horas inválidas", "400 Bad Request")
                return hora_on, hora_off, nombre

        elif 'GET /datos' in request_str:
            estado_led = pin_wifi_ok.value()
            datos = {
                "temp": temperatura,
                "hume": humedad,
                "estado": "Encendido" if estado_led else "Apagado"
            }
            enviar_respuesta(conn, "json", datos)

        elif 'GET /config' in request_str:
            datos = {
                "hora_on": "{:02d}:{:02d}".format(hora_on // 3600, (hora_on % 3600) // 60) if hora_on else "",
                "hora_off": "{:02d}:{:02d}".format(hora_off // 3600, (hora_off % 3600) // 60) if hora_off else "",
                "nombre": nombre
            }
            enviar_respuesta(conn, "json", datos)

        elif 'GET' in request_str:
            html = pagina_guev(nombre)
            enviar_respuesta(conn, "html", html)

        else:
            enviar_respuesta(conn, "text", "Ruta no encontrada", "404 Not Found")

    except Exception as e:
        print("Error en manejar_peticion:", e)
        enviar_respuesta(conn, "text", "Error interno", "500 Internal Server Error")
    finally:
        conn.close()

    return hora_on, hora_off, nombre

def leer_sensor():
    try:
        return sensor.temperature, sensor.relative_humidity
    except OSError as e:
        print("error sensor", e)
        return None, None
