import os
import requests
import time

# ==============================
# 1️⃣ Variables de entorno
# ==============================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
API_KEY = os.environ.get("API_KEY")
YOUTUBE_CHANNEL_ID = os.environ.get("YOUTUBE_CHANNEL_ID")
ARCHIVO_VALOR = "ultimo_valor.txt"

# ==============================
# 2️⃣ Función para obtener suscriptores de YouTube
# ==============================
def obtener_suscriptores():
    """
    Obtiene el número de suscriptores del canal de YouTube usando la API oficial
    """
    try:
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={YOUTUBE_CHANNEL_ID}&key={API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if "items" in data and len(data["items"]) > 0:
            suscriptores = int(data["items"][0]["statistics"]["subscriberCount"])
            return suscriptores
        else:
            print("Error: No se encontró el canal")
            return None
    except Exception as e:
        print(f"Error al obtener suscriptores: {e}")
        return None

# ==============================
# 3️⃣ Crear archivo si no existe
# ==============================
if not os.path.exists(ARCHIVO_VALOR):
    with open(ARCHIVO_VALOR, "w") as f:
        f.write("302")

# ==============================
# 4️⃣ Loop principal
# ==============================
print("Bot iniciado. Monitoreando suscriptores...")

while True:
    try:
        # Leer último valor guardado
        with open(ARCHIVO_VALOR, "r") as f:
            ultimo_valor = int(f.read())

        valor_actual = obtener_suscriptores()

        if valor_actual is None:
            print("No se pudo obtener el valor actual, reintentando...")
            time.sleep(30)
            continue

        print(f"Último valor: {ultimo_valor}, Valor actual: {valor_actual}")

        # Comparar con el valor anterior
        if valor_actual != ultimo_valor:
            # Guardar nuevo valor
            with open(ARCHIVO_VALOR, "w") as f:
                f.write(str(valor_actual))

            # Enviar notificación a Telegram
            mensaje = f"🎉 ¡Cambio detectado! Suscriptores: {valor_actual}"
            url_telegram = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mensaje}"
            requests.get(url_telegram)
            print(f"Notificación enviada: {mensaje}")

        # Espera 60 segundos antes de la siguiente revisión
        time.sleep(60)

    except Exception as e:
        print(f"Error en el loop principal: {e}")
        time.sleep(60)
