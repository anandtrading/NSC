import requests
TELEGRAM_BOT_TOKEN = "YOUR_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

def send_msg(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"})

def get_spot():
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EBSESN?range=1d&interval=1m"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()
        closes = [x for x in r['chart']['result'][0]['indicators']['quote'][0]['close'] if x is not None]
        return closes[-1]
    except:
        return 73300

spot = get_spot()

if spot < 73100:
    signal = "🔴 PUT BUY - 73300 PUT எடு! Target 200!"
elif spot > 73500:
    signal = "🟢 CALL BUY - 73600 CALL எடு! Target 200!"
else:
    signal = "🟡 WAIT - Sideways! Trade வேண்டாம்!"

msg = f"🚀 Sensex: {spot:.0f}\n{signal}\nTime: 9:10 AM"
send_msg(msg)
print(msg)
