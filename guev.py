def pagina_guev(nombre="GrowBox"):
    html = """<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{nombre}</title>
    <link rel="stylesheet" href="https://unpkg.com/chota@latest" />
    <style>
      body {{
        background-image: url("https://lh3.googleusercontent.com/pw/AIL4fc8aqICJOGtWal8Q1Ghbze4NhdCun-2Elm36Sf0jyHnGVepzN9qDblrD104rAtDmtDG_7fl8nsMEs-BRef2YvkHvZTv4FexcyMezTowz7IykpQCsLbNv7mWwdOe3-0p8kGSoskQE7FUPEhYx-Yco7ptUVg=w748-h1580-s-no");
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-size: cover;
        padding: 20px;
      }}
      body.dark {{
        --bg-color: #000;
        --bg-secondary-color: #131316;
        --font-color: #f5f5f5;
      }}
      .card {{
        background: #000000b5;
        padding: 20px;
        max-width: 400px;
        margin: 20px auto;
        text-align: center;
        border-radius: 10px;
      }}
      .titulo {{
        text-align: center;
        margin-bottom: 20px;
      }}
      .dato {{
        font-size: 2rem;
        margin: 10px 0;
      }}
      label {{
        display: block;
        margin: 10px 0 5px;
      }}
      input[type="time"], input[type="text"] {{
        width: 70%;
        display: block;
        margin: 0 auto 10px auto;
      }}
    </style>
  </head>
  <body class="dark">
    <h1 class="titulo" id="nombre-growbox">{nombre}</h1>

    <div class="card">
      <h2 class="dato">Datos del ambiente</h2>
      <p id="temp" class="dato">Temperatura: -- °C</p>
      <p id="hume" class="dato">Humedad: -- %</p>
    </div>

    <div class="card">
      <h2 class="dato">Control de Iluminación</h2>
      <p class="dato" id="estado">Estado: <span id="estado-valor">--</span></p>
      <label>Hora de encendido:</label>
      <input type="time" id="hora-on" />
      <label>Hora de apagado:</label>
      <input type="time" id="hora-off" />
      <br/>
      <button class="button primary" onclick="enviarHoras()">Guardar</button>
    </div>

    <div class="card">
      <h2 class="dato">Cambiar Nombre</h2>
      <label>Nombre del sistema:</label>
      <input type="text" id="nombre" placeholder="GrowBox" />
      <br/>
      <button class="button primary" onclick="enviarHoras()">Guardar</button>
    </div>

    <div id="toast" style="
      visibility: hidden;
      min-width: 200px;
      background-color: #333;
      color: #fff;
      text-align: center;
      border-radius: 4px;
      padding: 8px 12px;
      position: fixed;
      z-index: 1000;
      left: 50%;
      bottom: 30px;
      transform: translateX(-50%);
      font-size: 14px;
      opacity: 0;
      transition: opacity 0.5s, visibility 0.5s;
    "></div>

    <script>
      function actualizarDatos() {{
        fetch('/datos')
          .then(response => response.json())
          .then(data => {{
            document.getElementById('temp').innerText = 'Temperatura: ' + data.temp + ' °C';
            document.getElementById('hume').innerText = 'Humedad: ' + data.hume + ' %';
            const estadoElem = document.getElementById('estado-valor');
            estadoElem.innerText = data.estado;
            estadoElem.style.color = data.estado === 'Encendido' ? 'lime' : 'tomato';
          }});
      }}

      function enviarHoras() {{
        const on = document.getElementById("hora-on").value;
        const off = document.getElementById("hora-off").value;
        const nombre = document.getElementById("nombre").value;
        if (!on || !off || !nombre) {{
          toast("Completá todos los campos.");
          return;
        }}
        fetch('/horas', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ encender: on, apagar: off, nombre: nombre }})
        }}).then(() => {{
          document.getElementById("nombre-growbox").innerText = nombre;
          toast("Configuración guardada correctamente");
        }}).catch(() => {{
          toast("Error al guardar configuración");
        }});
      }}

      function cargarConfiguracion() {{
        fetch('/config')
          .then(response => response.json())
          .then(data => {{
            if (data.hora_on) document.getElementById("hora-on").value = data.hora_on;
            if (data.hora_off) document.getElementById("hora-off").value = data.hora_off;
            if (data.nombre) {{
              document.getElementById("nombre").value = data.nombre;
              document.getElementById("nombre-growbox").innerText = data.nombre;
            }}
          }});
      }}

      function toast(mensaje, color = "#333") {{
        const x = document.getElementById("toast");
        x.textContent = mensaje;
        x.style.backgroundColor = color;
        x.style.visibility = "visible";
        x.style.opacity = "1";
        setTimeout(() => {{
          x.style.opacity = "0";
          x.style.visibility = "hidden";
        }}, 3000);
      }}

      actualizarDatos();
      cargarConfiguracion();
      setInterval(actualizarDatos, 5000);
    </script>
  </body>
</html>
""".format(nombre=nombre)
    return html
