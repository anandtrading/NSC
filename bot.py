import requests

TELEGRAM_BOT_TOKEN = "YOUR_NEW_TOKEN_HERE"
TELEGRAM_CHAT_ID = "7995294715"

def send_msg(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print(e)

def get_yahoo_price(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=1d&interval=1m"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).json()
        meta = r['chart']['result'][0]['meta']
        price = meta['regularMarketPrice']
        prev = meta['chartPreviousClose']
        ch = price - prev
        pct = (ch / prev) * 100
        return price, ch, pct
    except:
        return 0,0,0

# Data Fetch
dow_p, dow_c, dow_pct = get_yahoo_price("%5EDJI")
nas_p, nas_c, nas_pct = get_yahoo_price("%5EIXIC")
gift_p, gift_c, gift_pct = get_yahoo_price("%5ENSEI") # GIFT Nifty Proxy Nifty 50
bank_p, bank_c, bank_pct = get_yahoo_price("%5ENSEBANK") # Bank Nifty
nifty_p, nifty_c, nifty_pct = get_yahoo_price("%5ENSEI")
crude_p, crude_c, crude_pct = get_yahoo_price("BZ=F") # Brent Crude

# Pro Scoring
score = 0
reasons = []

# 1. GIFT Logic
if gift_pct > 0.3: 
    score += 2
    reasons.append(f"GIFT Up {gift_pct:+.2f}%")
elif gift_pct < -0.3:
    score -= 2
    reasons.append(f"GIFT Down {gift_pct:+.2f}%")

# 2. BankNifty Strong Logic - இன்னைக்கு நடந்தது மாதிரி
if bank_pct > nifty_pct + 0.3:
    score += 2
    reasons.append(f"Bank Strong {bank_pct:+.2f}% > Nifty {nifty_pct:+.2f}% => Recovery Chance")
elif bank_pct < nifty_pct - 0.3:
    score -= 1
    reasons.append(f"Bank Weak")

# 3. Crude Oil Logic
if crude_p > 115:
    score -= 2
    reasons.append(f"Crude High ${crude_p:.0f} Bearish")
else:
    score += 1
    reasons.append(f"Crude Ok ${crude_p:.0f}")

# 4. US Market
if dow_pct > 0.2 and nas_pct > 0.3:
    score += 1
    reasons.append(f"US Up Dow {dow_pct:+.2f}%")

# Final Decision
if score >= 2:
    action = "🟢 *PRO BOT: CALL BUY - RECOVERY EXPECTED*\n🎯 Target: BankNifty Support + Auto Buying"
    strike = "Sensex 73500 CALL / BankNifty 55500 CALL"
elif score <= -2:
    action = "🔴 *PRO BOT: PUT BUY - GAP DOWN CONTINUE*\n🎯 Crude + FPI Selling Pressure"
    strike = "Sensex 73300 PUT / Nifty 22700 PUT"
else:
    action = "🟡 *PRO BOT: WAIT & WATCH - MIXED*\n9:25 வரை BankNifty-ஐ பாரு"
    strike = "No Trade Now"

msg = f"""🚀 *ANAND PRO WORLD + SECTOR BOT*
⏰ Signal

🌍 GIFT: {gift_pct:+.2f}% | {gift_p:.0f}
🏦 Bank: {bank_pct:+.2f}% | Nifty: {nifty_pct:+.2f}%
🛢️ Crude: ${crude_p:.0f}
🇺🇸 US Dow: {dow_pct:+.2f}% | Nasdaq: {nas_pct:+.2f}%

📊 *Logic:*
{chr(10).join(['- '+r for r in reasons])}

{action}
💰 Strike: {strike}
Score: {score}
"""

send_msg(msg)
print("Pro Bot Done")
