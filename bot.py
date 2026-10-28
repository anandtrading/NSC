import requests

# உன் Telegram Details - மாத்தாதே, ஏற்கனவே இருக்குறதே இருக்கட்டும்
TELEGRAM_BOT_TOKEN = "9045379420:AAHi0JGX_rMwUhaHbwAf3dOSrkOwyzdo8lo"
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
        prev_close = meta['chartPreviousClose']
        change = price - prev_close
        change_pct = (change / prev_close) * 100
        return price, change, change_pct
    except:
        return 0, 0, 0

# World Market Data எடுக்குறோம்
dow_price, dow_change, dow_pct = get_yahoo_price("%5EDJI")  # Dow Jones
nasdaq_price, nasdaq_change, nasdaq_pct = get_yahoo_price("%5EIXIC") # Nasdaq
sp_price, sp_change, sp_pct = get_yahoo_price("%5EGSPC") # S&P 500
sensex_price, sensex_change, sensex_pct = get_yahoo_price("%5EBSESN") # Sensex

# Scoring System
bear_score = 0
bull_score = 0

if dow_change < -100: bear_score += 2
elif dow_change > 100: bull_score += 2

if nasdaq_pct < -0.5: bear_score += 1
elif nasdaq_pct > 0.5: bull_score += 1

if sp_pct < -0.3: bear_score += 1
elif sp_pct > 0.3: bull_score += 1

# Final Signal Decision
if bear_score >= 2:
    signal = "🔴 *WORLD MARKET BEARISH - PUT BUY*\n🎯 73300 PUT எடு!\n💡 Target: 200 Pts\n⚠️ US Market Down-னால India-வும் Down!"
    trade_type = "PUT"
elif bull_score >= 2:
    signal = "🟢 *WORLD MARKET BULLISH - CALL BUY*\n🎯 73600 CALL எடு!\n💡 Target: 200 Pts\n🚀 US Market Up-னால India-வும் Up!"
    trade_type = "CALL"
else:
    signal = "🟡 *MIXED SIGNALS - WAIT*\nWorld Market Sideways, 9:30 வரை Wait!"
    trade_type = "WAIT"

msg = f"""🚀 *ANAND WORLD MARKET BOT*
⏰ 9:10 AM Signal

🌍 *WORLD MARKET:*
🇺🇸 Dow: {dow_change:+.0f} ({dow_pct:+.2f}%)
💻 Nasdaq: {nasdaq_pct:+.2f}%
📊 S&P 500: {sp_pct:+.2f}%

📍 *INDIA:*
Sensex: {sensex_price:.0f} ({sensex_change:+.0f})

{signal}
"""

send_msg(msg)
print("Done")
