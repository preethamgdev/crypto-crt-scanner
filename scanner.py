import requests

symbols = [
    'BTCUSDT',
    'ETHUSDT',
    'SOLUSDT',
    'XRPUSDT',
    'DOGEUSDT',
    'SUIUSDT',
    'LINKUSDT',
    'AVAXUSDT',
    'ADAUSDT',
    'WIFUSDT'
]

results = []

for symbol in symbols:

    try:

        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1d&limit=3"

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        data = response.json()

        if not isinstance(data, list):
            print(f"Invalid response for {symbol}")
            continue

        if len(data) < 3:
            continue

        prev = data[-3]
        yest = data[-2]

        low_2 = float(prev[3])
        low_1 = float(yest[3])
        close_1 = float(yest[4])

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
