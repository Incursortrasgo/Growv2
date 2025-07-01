import time
import ujson
import ahtx0
from machine import I2C, Pin
from guev import pagina_guev

# Inicialización de I2C y sensor
i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000)
sensor = ahtx0.AHT10(i2c)

def hora_a_segundos(hora_str):
    try:
        h, m = map(int, hora_str.split(":"))
        return h * 3600 + m * 60
    except:
        return None

def hora_actual_segundos():
    t = time.localtime(time.time() - 3 * 3600)  # UTC-3
    return t[3] * 3600 + t[4] * 60

def guardar_config(hora_on, hora_off):
    config = {
        "hora_on": hora_on,
        "hora_off": hora_off
    }
    with open("config.json", "w") as f:
        ujson.dump(config, f)

def cargar_config():
    try:
        with open("config.json", "r") as f:
            config = ujson.load(f)
            hora_on = config.get("hora_on")
            hora_off = config.get("hora_off")
            print("Configuración cargada:", hora_on, hora_off)
            return hora_on, hora_off
    except:
        print("No se encontró configuración previa.")
        return None, None

def manejar_peticion(conn, addr, temperatura, humedad, hora_on, hora_off):
    print("-----------------")
    print("Got a Connection")
    print("Temp: ", temperatura)
    print("Hum: ", humedad)
    request = conn.recv(1024)
    request_str = request.decode()

    if 'POST /horas' in request_str:
        cuerpo = request_str.split("\r\n\r\n")[1]
        datos = ujson.loads(cuerpo)
        hora_on = hora_a_segundos(datos.get("encender", ""))
        hora_off = hora_a_segundos(datos.get("apagar", ""))
        guardar_config(hora_on, hora_off)
        print("Guardado hora_on:", hora_on, "hora_off:", hora_off)

        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/plain\n')
        conn.send('Connection: close\n\n')
        conn.sendall(b'OK')

    elif 'GET /datos' in request_str:
        datos = ujson.dumps({"temp": temperatura, "hume": humedad})
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: application/json\n')
        conn.send('Connection: close\n\n')
        conn.sendall(datos)

    elif 'GET /config' in request_str:
        datos = ujson.dumps({
            "hora_on": "{:02d}:{:02d}".format(hora_on // 3600, (hora_on % 3600) // 60) if hora_on is not None else "",
            "hora_off": "{:02d}:{:02d}".format(hora_off // 3600, (hora_off % 3600) // 60) if hora_off is not None else ""
        })
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: application/json\n')
        conn.send('Connection: close\n\n')
        conn.sendall(datos)

    else:
        response = pagina_guev()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)

    conn.close()
    return hora_on, hora_off

def leer_sensor():
    try:
        temperatura = sensor.temperature
        humedad = sensor.relative_humidity
    except OSError as e:
        temperatura = 0.0
        humedad = 0.0
        print("error sensor", e)

    return (temperatura, humedad)
