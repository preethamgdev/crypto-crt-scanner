import requests
import json

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

for symbol in allowed_symbols:

    try:

        url = "https://api.bybit.com/v5/market/kline"

        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": "D",
            "limit": 3
        }

        response = requests.get(
            url,
            params=params,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        # Convert safely
        data = json.loads(response.text)

        if 'result' not in data:
            print(f"No result for {symbol}")
            continue

        candles = data['result']['list']

        if len(candles) < 3:
            continue

        # Bybit newest candle first
        yest = candles[1]
        prev = candles[2]

        low_1 = float(yest[3])
        close_1 = float(yest[4])

        low_2 = float(prev[3])

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
