import requests


def get_tiprank_for_ticker(ticker):
    score = 0
    try:
        url = "https://www.tipranks.com/api/stocks/stockAnalysisOverview/?tickers=" + ticker

        url = requests.get(url)
        result = url.json()
        # score = result[0]['smartScore']
        # momentum = result[0]['technicalsTwelveMonthsMomentum']
    except:
        # score = None
        # momentum = None
        pass
    return result[0] if len(result) > 0 else None


if __name__ == '__main__':
    tr = get_tiprank_for_ticker('ABCL')
