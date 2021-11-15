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
    today = datetime.datetime.now().date()
    year_ago = (datetime.datetime.now() - datetime.timedelta(days=365)).date()
    url = (
            "https://financialmodelingprep.com/api/v3/historical-price-full/" + t + "?from=" + str(
        year_ago) + "&to=" + str(today) + "&apikey=" + FMP_KEY)
    data = get_jsonparsed_data(url)
    # print(get_jsonparsed_data(url))
    return data['historical']


def get_last_year_full_for_ticker(t):
    # used in spider
    days = 365
    url = (
            "https://financialmodelingprep.com/api/v3/historical-price-full/" + t + "?timeseries=" + str(
        days) + "&apikey=" + FMP_KEY)
    data = get_jsonparsed_data(url)
    print("got Last year data  from FMP for : " + t)
    return data['historical']


def historical_daily_price_full_w(t):
    # wrapper for ticker info
    url = (
            "https://financialmodelingprep.com/api/v3/historical-price-full/" + t + "?serietype=line&apikey=" + FMP_KEY)
    context = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(url, context=context)
    data = json.load(response)
    return data


def current_market_operation_w():
    # wrapper for current us market open/closed state
    url = (
            "https://financialmodelingprep.com/api/v3/is-the-market-open?apikey=" + FMP_KEY)
    data = get_jsonparsed_data(url)
    toJson = json.dumps(data)
    return toJson


def get_company_info_for_ticker(t):
    # used on adding ticker
    url = (
            f"https://financialmodelingprep.com/api/v3/profile/{t}?apikey={FMP_KEY}")
    data = get_jsonparsed_data(url)
    return data[0] if len(data) > 0 else None


def current_stock_price_full_w(t):
    #wrapper for current us market open/closed state
    url = (
        "https://financialmodelingprep.com/api/v3/quote/"+t+"?apikey="+FMP_KEY)
    data=get_jsonparsed_data(url)
    toJson=json.dumps(data)
    return toJson

def current_stock_price_short_w(t):
    #wrapper for current us market open/closed state
    url = (
        "https://financialmodelingprep.com/api/v3/quote-short/"+t+"?apikey="+FMP_KEY)
    data=get_jsonparsed_data(url)
    toJson=json.dumps(data)
    return toJson

if __name__ == '__main__':
    get_last_year_full_for_ticker('msft')




