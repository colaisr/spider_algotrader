import json
import ssl
import urllib
from urllib.request import urlopen
from datetime import datetime
import time
import yfinance as yf

server_url = "http://colak.eu.pythonanywhere.com/"
# server_url = "http://localhost:8000/"


def get_all_tickers():
    print("Getting all necessary tickers from Algotrader server")
    _url = (f"{server_url}research/alltickers")
    _context = ssl._create_unverified_context()
    _response = urlopen(_url, context=_context)
    _data = _response.read().decode("utf-8")
    _parsed = json.loads(_data)
    print(f"Got all {str(len(_parsed))} tickers from server- starting to update...")
    return _parsed

now = datetime.now()
print("*************************************************")
print(f"****Starting spider for last week champs {now.strftime('%d/%m/%Y %H:%M:%S')} ****")
tickers = get_all_tickers()

for t in tickers:
    start_update_time = time.time()
    print(f'Updating data for : {t} stamp: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
    data = urllib.parse.urlencode({"ticker_to_update": t})
    data = _data.encode('ascii')
    url = server_url + "candidates/replace_yahoo_data"
    response = urllib.request.urlopen(url, data)
    end_update_time = time.time()
    print(f"Updated stamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

