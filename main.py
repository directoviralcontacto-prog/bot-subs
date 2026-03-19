import requests
import time
import os


API_KEY = os.environ.get("API_KEY")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

print("Variables cargadas correctamente")  # Solo para probar


API_KEY = os.getenv("API_KEY")
CHANNEL_ID = "UCTkZ8ndFFPI5dPEZHAhw-VA"  # tu channel id

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_subs():
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={API_KEY}"
    r = requests.get(url)
    data = r.json()
    
    if "items" not in data:
        print("ERROR API:", data)
        return None
    
    return int(data["items"][0]["statistics"]["subscriberCount"])

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    
    if r.status_code != 200:
        print("ERROR TELEGRAM:", r.text)

last = get_subs()
print("Subs iniciales:", last)

while True:
    time.sleep(60)
    current = get_subs()
    
    if current and last and current != last:
        diff = current - last
        msg = f"Subs: {current} ({'+' if diff>0 else ''}{diff})"
        
        print("Cambio detectado:", msg)
        send_msg(msg)
        
        last = current

