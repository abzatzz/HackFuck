from binance.client import Client
import keys
import pandas as pd
import time

client = Client(keys.api_key_real, keys.secret_key_real)

all_tickers = client.get_ticker('symbol')


