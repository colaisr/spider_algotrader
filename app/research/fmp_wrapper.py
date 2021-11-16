import datetime
import os
import ssl
from urllib.request import urlopen
import certifi
import json

FMP_KEY = os.environ.get("FMP_KEY")


def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    context = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    return json.loads(data)


def get_last_year_full_for_ticker_optional(t):
    today=datetime.datetime.now().date()
    year_ago=(datetime.datetime.now() - datetime.timedelta(days=365)).date()
    url = (
        "https://financialmodelingprep.com/api/v3/historical-price-full/"+t+"?from="+str(year_ago)+"&to="+str(today)+"&apikey="+FMP_KEY)
    data=get_jsonparsed_data(url)
    # print(get_jsonparsed_data(url))
    return data['historical']

def get_last_year_full_for_ticker(t):
    #used in spider
    days=365
    url = (
        "https://financialmodelingprep.com/api/v3/historical-price-full/"+t+"?timeseries="+str(days)+"&apikey="+FMP_KEY)
    data=get_jsonparsed_data(url)
    print("got Last year data  from FMP for : "+t)
    return data['historical']

def historical_daily_price_full_w(t):
    #wrapper for ticker info
    url = (
        "https://financialmodelingprep.com/api/v3/historical-price-full/"+t+"?serietype=line&apikey="+FMP_KEY)
    data=get_jsonparsed_data(url)
    return data

def current_market_operation_w():
    #wrapper for current us market open/closed state
    url = (
        "https://financialmodelingprep.com/api/v3/is-the-market-open?apikey="+FMP_KEY)
    data=get_jsonparsed_data(url)
    return data

def get_company_info_for_ticker(t):
    #used on adding ticker
    url = (
        "https://financialmodelingprep.com/api/v3/profile/"+t+"?apikey="+FMP_KEY)
    data=get_jsonparsed_data(url)
    return data[0]

def current_stock_price_full_w(t):
    #wrapper for current us market open/closed state
    url = (
        "https://financialmodelingprep.com/api/v3/quote/"+t+"?apikey="+FMP_KEY)
    data=get_jsonparsed_data(url)
    return data

def current_stock_price_short_w(t):
    #wrapper for current us market open/closed state
    url = (
        "https://financialmodelingprep.com/api/v3/quote-short/"+t+"?apikey="+FMP_KEY)
    data=get_jsonparsed_data(url)
    return data

def stock_news_w(t,l):
    #wrapper for stock news
    url = (
        "https://financialmodelingprep.com/api/v3/stock_news?tickers="+t+"&limit="+str(l)+"&apikey="+FMP_KEY)
    data=get_jsonparsed_data(url)
    return data

def average_sector_pe_today(sector):
    #wrapper today pe average
    today=str(datetime.datetime.utcnow().date())
    url = (
        "https://financialmodelingprep.com/api/v4/sector_price_earning_ratio?date="+today+"&exchange=NYSE&apikey="+FMP_KEY)
    data=get_jsonparsed_data(url)
    for s in data:
        d=s['sector']
        if d==sector:
            return s
    return data

if __name__ == '__main__':
    get_last_year_full_for_ticker('msft')




