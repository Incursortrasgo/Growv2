🌱 Growv2 – Sistema de Automatización Indoor con ESP32
Growv2 es un sistema modular para monitoreo y control de entornos de cultivo indoor. Basado en MicroPython y ejecutándose en una placa ESP32, permite controlar luces y ver los parametros del ambiente (por ahora)


✨ Características
- Lectura de sensores ambientales (temperatura, humedad, luz, etc.)
- Control de dispositivos como luces, ventiladores o bombas de agua
- Interfaz web para visualización y configuración en tiempo real
- Persistencia de configuraciones entre reinicios
- Código ligero y fácil de adaptar


🔧 Requisitos
- Placa ESP32 con soporte para MicroPython
- Sensores compatibles (p. ej. DHT22, BH1750)
- Entorno de desarrollo como Thonny o ampy
- Conexión Wi-Fi para acceder al dashboard web


📦 Instalación
git clone https://github.com/Incursortrasgo/Growv2.git
- Flasheá MicroPython en el ESP32 (si no lo hiciste antes).
- Subí los archivos .py al dispositivo.

🪜 Pasos para conectar:
- Encendé el ESP32. Si no hay una red guardada, se activará un Access Point llamado, GrowBox WiFi
- Conectate desde tu PC o celular a esa red Wi-Fi (no requiere contraseña).
- Abrí el navegador y accedé a la dirección: http://192.168.4.1
- Elegí tu red Wi-Fi doméstica de la lista que aparece y escribí tu contraseña.
- El ESP32 guardará esa red y se reiniciará conectado a ella automáticamente.
- Espera en la web que te dirá cual es la dirección de tu nuevo GrowBox
- Conectate a esa dirección desde cualquier dispositivo con acceso a tu red domestica


  
📁 Estructura del proyecto
Growv2/
├── main.py         # Script principal
├── sensors.py      # Módulo para sensores
├── webserver.py    # Interfaz web
└── README.md


📍 Próximas mejoras
- Soporte para notificaciones vía Telegram o email
- Guardado de historial de datos
- Configuración remota desde el dashboard
📝 Licencia
Este proyecto está licenciado bajo los términos de la licencia MIT.

Desarrollado como 💡 por @Incursortrasgo

