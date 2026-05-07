import yfinance as yf
import requests
BOT_TOKEN = "8025462243:AAHJjDknO0rSKY493vFJMz9LVPBHB0KP1dw"
CHAT_ID = "5270296136"
symbols = [
    "BTC-USD",
    "ETH-USD",
    "SOL-USD",
    "XRP-USD",
    "DOGE-USD",
    "SUI20947-USD",
    "LINK-USD",
    "AVAX-USD",
    "ADA-USD"
]

results = []

for symbol in symbols:

    try:

        df = yf.download(
            symbol,
            period="7d",
            interval="1d",
            progress=False,
            auto_adjust=False
        )

        if len(df) < 3:
            continue

        # Yesterday candle
        yest = df.iloc[-2]

        # Previous candle
        prev = df.iloc[-3]

        low_1 = yest["Low"].item()
        close_1 = yest["Close"].item()

        low_2 = prev["Low"].item()

        # Bullish CRT
        if low_1 < low_2 and close_1 > low_2:

            results.append(symbol)

    except Exception as e:

        print(f"Error with {symbol}: {e}")

print("\n🔥 Bullish CRT Coins 🔥\n")

if len(results) == 0:

    print("No bullish CRT setups today.")

else:

    for r in results:

        print(r)
# =========================
# TELEGRAM ALERT
# =========================

message = "🔥 Bullish CRT Coins 🔥\n\n"

if len(results) == 0:

    message += "No bullish CRT setups today."

else:

    for r in results:

        message += f"{r}\n"

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": message
}

requests.post(telegram_url, data=payload)

print("\nTelegram alert sent.")
