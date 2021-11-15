
import pandas as pd

from app.research.fmp_wrapper import get_last_year_full_for_ticker, get_company_info_for_ticker


def get_fmp_stats_for_ticker(s):
    df = get_last_year_full_for_ticker(s)
    max_intraday_drop_percent = 0
    avdropP = 0
    avChangeP = 0
    buying_target_price=0

    if len(df)>0:
        last_closing_adjusted_price=df[0]['adjClose']
        df=pd.DataFrame(df)
        df['drop'] = df['open'] - df['low']
        df['dropP'] = df['drop'] / df['open'] * 100
        df['diffD'] = df['low'] - df['high']
        df['diffD'] = df['diffD'].abs()
        df['diffP'] = df['diffD'] / df['open'] * 100
        max_intraday_drop_percent = df['dropP'].max()
        avdropP = df["dropP"].mean()
        avChangeP = df["diffP"].mean()
        buying_target_price=last_closing_adjusted_price-(last_closing_adjusted_price/100*avdropP)

    return avdropP, avChangeP, max_intraday_drop_percent,buying_target_price


def get_company_info(s):
    inf = get_company_info_for_ticker(s)
    return inf


if __name__ == '__main__':
    a,b,c=get_fmp_stats_for_ticker('msft')
    r = 3
