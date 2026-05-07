
import requests

# =========================
# SETTINGS
# =========================

allowed_symbols = [
    'BTCUSDT',
    'ETHUSDT',
    'SOLUSDT',
    'XRPUSDT',
    'DOGEUSDT',
    'SUIUSDT',
    'LINKUSDT',
    'AVAXUSDT',
    'ADAUSDT',
    'WIFUSDT',
    '1000PEPEUSDT'
]

results = []

# =========================
# MAIN LOOP
# =========================

for symbol in allowed_symbols:

    try:

        url = "https://api.bybit.com/v5/market/kline"

        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": "D",
            "limit": 3
        }

        response = requests.get(url, params=params, timeout=10)

        data = response.json()

        if 'result' not in data:
            continue

        candles = data['result']['list']

        if len(candles) < 3:
            continue

        # Bybit returns newest first
        yest = candles[1]
        prev = candles[2]

        # Candle format:
        # [timestamp, open, high, low, close, volume, turnover]

        low_1 = float(yest[3])
        close_1 = float(yest[4])

        low_2 = float(prev[3])

        # Bullish CRT
        if low_1 < low_2 and close_1 > low_2:

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
