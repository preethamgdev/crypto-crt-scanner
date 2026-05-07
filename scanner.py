import requests
import sys

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

# =========================
# FETCH SYMBOLS SAFELY
# =========================

try:
    symbols_response = requests.get(symbols_url, timeout=10)
    symbols_json = symbols_response.json()

    if 'symbols' not in symbols_json:
        print("ERROR: Binance exchangeInfo API failed")
        print(symbols_json)
        sys.exit(1)

    symbols = symbols_json['symbols']

except Exception as e:
    print(f"ERROR fetching symbols: {e}")
    sys.exit(1)

# =========================
# FETCH TICKERS SAFELY
# =========================

try:
    tickers_response = requests.get(ticker_url, timeout=10)
    tickers = tickers_response.json()

except Exception as e:
    print(f"ERROR fetching tickers: {e}")
    sys.exit(1)

# =========================
# VOLUME DICTIONARY
# =========================

volume_dict = {}

for t in tickers:

    if 'symbol' in t and 'quoteVolume' in t:

        try:
            volume_dict[t['symbol']] = float(t['quoteVolume'])
        except:
            continue

# =========================
# MAIN SCAN
# =========================

results = []

for s in symbols:

    try:

        if s.get('contractType') != 'PERPETUAL':
            continue

        if s.get('quoteAsset') != 'USDT':
            continue

        symbol = s.get('symbol')

        if symbol not in allowed_symbols:
            continue

        if volume_dict.get(symbol, 0) < 30000000:
            continue

        params = {
            "symbol": symbol,
            "interval": "1d",
            "limit": 3
        }

        response = requests.get(
            klines_url,
            params=params,
            timeout=10
        )

        data = response.json()

        if not isinstance(data, list):
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

            results.append({
                'symbol': symbol,
                'volume': round(volume_dict[symbol] / 1000000, 2)
            })

    except Exception as e:
        print(f"Error scanning {s.get('symbol')}: {e}")
        continue

# =========================
# SORT RESULTS
# =========================

results = sorted(
    results,
    key=lambda x: x['volume'],
    reverse=True
)

# =========================
# OUTPUT
# =========================

print("\n🔥 Bullish CRT Coins 🔥\n")

if len(results) == 0:
    print("No bullish CRT setups today.")

else:

    for r in results:

        print(
            f"{r['symbol']} | "
            f"24H Volume: ${r['volume']}M"
        )
