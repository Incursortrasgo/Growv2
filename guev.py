def pagina_guev():
    html = """
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>GrowBox</title>
    <link rel="stylesheet" href="https://unpkg.com/chota@latest" />
    <style>
      body {
        background-image: url("https://lh3.googleusercontent.com/pw/AIL4fc8aqICJOGtWal8Q1Ghbze4NhdCun-2Elm36Sf0jyHnGVepzN9qDblrD104rAtDmtDG_7fl8nsMEs-BRef2YvkHvZTv4FexcyMezTowz7IykpQCsLbNv7mWwdOe3-0p8kGSoskQE7FUPEhYx-Yco7ptUVg=w748-h1580-s-no");
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-size: cover;
        padding: 20px;
      }
      body.dark {
        --bg-color: #000;
        --bg-secondary-color: #131316;
        --font-color: #f5f5f5;
      }
      .card {
        background: #000000b5;
        padding: 20px;
        max-width: 400px;
        margin: 20px auto;
        text-align: center;
        border-radius: 10px;
      }
      .titulo {
        text-align: center;
        margin-bottom: 20px;
      }
      .dato {
        font-size: 2rem;
        margin: 10px 0;
      }
      label {
        display: block;
        margin: 10px 0 5px;
      }
    </style>
  </head>
  <body class="dark">
    <h1 class="titulo">GrowBox</h1>

    <div class="card">
      <p id="temp" class="dato">Temperatura: -- °C</p>
      <p id="hume" class="dato">Humedad: -- %</p>
    </div>

    <div class="card">
      <p class="dato" id="hora-actual">Hora actual: --:--</p>
      <label>Hora de encendido:</label>
      <input type="time" id="hora-on">
      <label>Hora de apagado:</label>
      <input type="time" id="hora-off">
      <br/><br/>
      <button onclick="enviarHoras()">Guardar</button>
    </div>

    <script>
      function actualizarDatos() {
        fetch('/datos')
          .then(response => response.json())
          .then(data => {
            document.getElementById('temp').innerText = 'Temperatura: ' + data.temp + ' °C';
            document.getElementById('hume').innerText = 'Humedad: ' + data.hume + ' %';
          });
      }

      function actualizarHoraActual() {
        const ahora = new Date();
        const tiempo = ahora.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' });
        document.getElementById("hora-actual").innerText = "Hora actual: " + tiempo;
      }

      function enviarHoras() {
        const on = document.getElementById("hora-on").value;
        const off = document.getElementById("hora-off").value;

        fetch('/horas', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ encender: on, apagar: off })
        });
      }

      function cargarConfiguracion() {
        fetch('/config')
          .then(response => response.json())
          .then(data => {
            if (data.hora_on) document.getElementById("hora-on").value = data.hora_on;
            if (data.hora_off) document.getElementById("hora-off").value = data.hora_off;
          });
      }

      actualizarDatos();
      actualizarHoraActual();
      cargarConfiguracion();
      setInterval(actualizarDatos, 5000);
      setInterval(actualizarHoraActual, 1000);
    </script>
  </body>
</html>
"""
    return html
