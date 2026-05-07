import requests

symbols_url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
ticker_url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
klines_url = "https://fapi.binance.com/fapi/v1/klines"

allowed_symbols = [
    'BTCUSDT',
    'ETHUSDT',
    'SOLUSDT',
    'XRPUSDT',
    'BNBUSDT',
    'DOGEUSDT',
    'SUIUSDT',
    'LINKUSDT',
    'AVAXUSDT',
    'ADAUSDT',
    'WIFUSDT',
    '1000PEPEUSDT',
    'AAVEUSDT',
    'LTCUSDT',
    'UNIUSDT',
    'DOTUSDT',
    'NEARUSDT',
    'APTUSDT',
    'ARBUSDT',
    'OPUSDT'
]

symbols = requests.get(symbols_url).json()['symbols']
tickers = requests.get(ticker_url).json()

volume_dict = {}

for t in tickers:
    volume_dict[t['symbol']] = float(t['quoteVolume'])

results = []

for s in symbols:

    if s['contractType'] != 'PERPETUAL':
        continue

    if s['quoteAsset'] != 'USDT':
        continue

    symbol = s['symbol']

    if symbol not in allowed_symbols:
        continue

    if volume_dict.get(symbol, 0) < 30000000:
        continue

    params = {
        "symbol": symbol,
        "interval": "1d",
        "limit": 3
    }

    try:
        data = requests.get(klines_url, params=params).json()

        prev = data[-3]
        yest = data[-2]

        low_2 = float(prev[3])
        low_1 = float(yest[3])
        close_1 = float(yest[4])

        if low_1 < low_2 and close_1 > low_2:

            results.append({
                'symbol': symbol,
                'volume': round(volume_dict[symbol] / 1000000, 2)
            })

    except:
        continue

results = sorted(
    results,
    key=lambda x: x['volume'],
    reverse=True
)

print("\n🔥 Bullish CRT Coins 🔥\n")

if len(results) == 0:
    print("No bullish CRT setups today.")

else:
    for r in results:
        print(
            f"{r['symbol']} | "
            f"24H Volume: ${r['volume']}M"
        )
