import yfinance as yf


def get_yahoo_stats_for_ticker(s):
    df = yf.download(s, period="1y")
    max_intraday_drop_percent = 0
    avdropP = 0
    avChange = 0

    if not df.empty:
        df['drop'] = df['Open'] - df['Low']
        df['dropP'] = df['drop'] / df['Open'] * 100
        df['diffD'] = df['Low'] - df['High']
        df['diffD'] = df['diffD'].abs()
        df['diffP'] = df['diffD'] / df['Open'] * 100
        max_intraday_drop_percent = df['dropP'].max()
        avdropP = df["dropP"].mean()
        avChange = df["diffP"].mean()

    return avdropP, avChange, max_intraday_drop_percent


def get_info_for_ticker(s):
    # t=yf.Ticker(s)
    inf = yf.Ticker(s).info
    return inf


if __name__ == '__main__':
    #get_snp500_fails_intraday_lower_than(-3)
    get_info_for_ticker('msft')
    r = 3
