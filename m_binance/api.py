import ccxt
import os
from dotenv import load_dotenv


class Api:
    def __init__(self):
        load_dotenv()
        api_key = os.environ.get('BINANCE_API_KEY')
        secret = os.environ.get('BINANCE_SECRET_KEY')

        self.binance = ccxt.binance(config={
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future'
            }
        })

    def load_markets(self):
        markets = self.binance.load_markets()
        for m in markets:
            print(m)

    def present_price(self):
        symbol = "BTC/USDT"
        btc = self.binance.fetch_ticker(symbol)
        return btc['last']
