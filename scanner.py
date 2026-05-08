import yfinance as yf
import requests
import os

# =========================
# TELEGRAM SECRETS
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# COINS TO SCAN
# =========================

symbols = [
    "BTC-USD",
    "ETH-USD",
    "SOL-USD",
    "XRP-USD",
    "DOGE-USD",
    "LINK-USD",
    "AVAX-USD",
    "ADA-USD",
    "SUI20947-USD"
]

# =========================
# STORE RESULTS
# =========================

results = []

# =========================
# MAIN SCAN LOOP
# =========================

for symbol in symbols:

    try:

        # Fetch daily data
        df = yf.download(
            symbol,
            period="10d",
            interval="1d",
            progress=False,
            auto_adjust=False
        )

        # Need minimum candles
        if len(df) < 4:
            continue

        # =========================
        # FULLY CLOSED CANDLES
        # =========================

        prev = df.iloc[-3]   # Previous candle
        yest = df.iloc[-2]   # Latest closed candle

        # =========================
        # OHLC VALUES
        # =========================

        low_1 = yest["Low"].item()
        high_1 = yest["High"].item()
        open_1 = yest["Open"].item()
        close_1 = yest["Close"].item()

        low_2 = prev["Low"].item()
        high_2 = prev["High"].item()

        # =========================
        # TRUE BULLISH CRT
        # =========================

        bullish_crt = (
            low_1 < low_2 and           # Sweep previous low
            close_1 > low_2 and        # Reclaim above prev low
            close_1 < high_2 and       # Close inside prev range
            close_1 > open_1           # Green bullish candle
        )

        if bullish_crt:

            results.append(symbol)

    except Exception as e:

        print(f"Error with {symbol}: {e}")

# =========================
# OUTPUT
# =========================

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

response = requests.post(telegram_url, data=payload)

print("\nTelegram alert sent.")
print(response.text)
