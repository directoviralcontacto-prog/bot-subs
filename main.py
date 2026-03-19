import os
import requests
import time

# ==============================
# 1️⃣ Configura estas variables
# ==============================
# Estos se leen de tus Secrets en Railway, no hace falta cambiar aquí si ya los añadiste
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Tu token del bot de Telegram
CHAT_ID = os.environ.get("CHAT_ID")      # Tu chat ID de Telegram
ARCHIVO_VALOR = "ultimo_valor.txt"       # Archivo donde guardamos el último valor

# ==============================
# 2️⃣ Función para obtener el valor
# ==============================
def obtener_valor():
    """
    Aquí debes poner la lógica real para obtener el número de suscriptores
    o cualquier valor que quieras monitorear.
    """
    # EJEMPLO: reemplaza esta línea con la llamada a la API de YouTube
    return 118  # <-- Cambia esto según tu lógica real

# ==============================
# 3️⃣ Crear archivo si no existe
# ==============================
if not os.path.exists(ARCHIVO_VALOR):
    with open(ARCHIVO_VALOR, "w") as f:
        f.write("0")

# ==============================
# 4️⃣ Loop principal
# ==============================
while True:
    # Leer último valor guardado
    with open(ARCHIVO_VALOR, "r") as f:
        ultimo_valor = int(f.read())

    valor_actual = obtener_valor()

    # Comparar con el valor anterior
    if valor_actual != ultimo_valor:
        # Guardar nuevo valor
        with open(ARCHIVO_VALOR, "w") as f:
            f.write(str(valor_actual))

        # Enviar notificación a Telegram
        mensaje = f"¡Cambio detectado! Suscriptores: {valor_actual}"
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mensaje}")

    # Espera 30 segundos antes de la siguiente revisión
    time.sleep(30)
