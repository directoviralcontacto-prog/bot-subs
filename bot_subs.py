import requests
import time

API_KEY = "AIzaSyAc84fRZ51Bfr_mt_KyekyMCwfndT8U-xo"
CHANNEL_ID = "UCTkZ8ndFFPI5dPEZHAhw-VA"

TOKEN = "8672317158:AAEV5xsuYEPgW0WMe4-9l8vTXaBypMRJhCw"
CHAT_ID = "6904712563"

def get_subs():
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={API_KEY}"
    r = requests.get(url)
    data = r.json()
    
    return int(data["items"][0]["statistics"]["subscriberCount"])

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

last = get_subs()
print("Subs iniciales:", last)

while True:
    time.sleep(60)
    current = get_subs()
    
    if current != last:
        diff = current - last
        send_msg(f"Cambio de subs: {current} ({'+' if diff>0 else ''}{diff})")
        print("Cambio detectado:", current)
        last = current
