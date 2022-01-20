from sqlalchemy import text
from flask import (
    Blueprint,
    request
)

from app import csrf, db
import app.generalutils as general
from app.email import send_email
from app.models import Candidate, UserSetting, TickerData
from app.research.fmp_wrapper import *
from app.research.views import research_ticker, get_info_for_ticker
from app.research.tipranks_research import get_tiprank_for_ticker

from flask_cors import cross_origin

candidates = Blueprint('candidates', __name__)


@candidates.route('updatecandidate/', methods=['POST'])
@csrf.exempt
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def updatecandidate():
    result = {"color_status": "success", "message": "Ticker updated"}
    try:
        c = Candidate()
        c.ticker = request.form['ticker']
        c.reason = request.form['reason']
        c.email = request.form['email']
        c.enabled = True
        fill_ticker_data_from_fmp(c, True)
    except Exception as e:
        result = {"color_status": "danger", "message": "Error in server"}
    return json.dumps(result)
    # return redirect(url_for('candidates.usercandidates'))
    # return "success"


@candidates.route('add_candidate', methods=['POST'])
@csrf.exempt
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def add_candidate():
    result = {"color_status": "success", "message": "Ticker updated"}
    try:
        c = Candidate()
        c.ticker = request.form['ticker']
        c.reason = request.form['reason']
        c.email = request.form['email']
        c.enabled = True
        fill_ticker_data_from_fmp(c, False)
    except Exception as e:
        result = {"color_status": "danger", "message": "Error in server"}
    return json.dumps(result)
    # return redirect(url_for('candidates.usercandidates'))
    # return "success"


@candidates.route('add_by_spider', methods=['POST'])
@csrf.exempt
def add_by_spider():
    ticker_to_add = request.form['ticker_to_add']
    try:
        candidate = Candidate.query.filter_by(email='support@stockscore.company', ticker=ticker_to_add).first()
        if candidate is None:
            print('adding ' + ticker_to_add)
            c = Candidate()
            c.ticker = ticker_to_add
            c.reason = ""
            c.email = 'support@stockscore.company'
            c.enabled = True
            if not fill_ticker_data_from_fmp(c, True):
                print(ticker_to_add + " skept no FMP data...")
                return "skept candidate"
            return "success"
        else:
            return "candidate exist"
    except:
        send_email(recipient='support@stockscore.company',
                   subject='Algotrader adding candidate problem with ' + ticker_to_add,
                   template='account/email/research_issue',
                   ticker=ticker_to_add,
                   sections="")
        print("failed to add candidate")
        return "exception in candidate " + ticker_to_add
    # else:
    #     print("skept-exist")
    #     return "skept"


@candidates.route('update_ticker_historical', methods=['POST'])
@csrf.exempt
def update_ticker_historical():
    try:
        candidates = Candidate.query.all()
        if candidates is not None:
            for c in candidates:
                candidate_data = get_company_info_for_ticker(c.ticker)
                if candidate_data is not None:
                    c.company_name = candidate_data['companyName']
                    c.full_description = candidate_data['description']
                    c.exchange = candidate_data['exchange']
                    c.exchange_short = candidate_data['exchangeShortName']
                    c.industry = candidate_data['industry']
                    c.sector = candidate_data['sector']
                    c.logo = candidate_data['image']
                    c.website = candidate_data['website']
                    c.update_candidate()
    except Exception as e:
        print(e)
    return "updated"


def fill_ticker_data_from_fmp(c, research):
    candidate_data = get_company_info_for_ticker(c.ticker)
    tiprank_data = get_tiprank_for_ticker(c.ticker)
    if candidate_data is None or tiprank_data is None or len(candidate_data) == 0 \
            or candidate_data['cik'] is None \
            or candidate_data['cik'] == '' \
            or candidate_data['isEtf'] \
            or candidate_data['exchange'] =='Other OTC'\
            or not candidate_data['isActivelyTrading']:
        return False
    else:
        c.company_name = candidate_data['companyName']
        c.full_description = candidate_data['description']
        c.exchange = candidate_data['exchange']
        c.exchange_short = candidate_data['exchangeShortName']
        c.industry = candidate_data['industry']
        c.sector = candidate_data['sector']
        c.logo = candidate_data['image']
        c.website = candidate_data['website']
        c.isActivelyTrading_fmp = candidate_data['isActivelyTrading']
        c.update_candidate()
        if research:
            research_ticker(c.ticker)
        return True


@candidates.route('notifications', methods=['GET'])
@csrf.exempt
def notifications():
    users = UserSetting.query.filter_by(notify_candidate_signal=1).all()
    for user in users:
        query_text = f"SELECT a.ticker, a.buying_target_price_fmp " \
                     f"FROM Tickersdata a JOIN " \
                     f"(SELECT t.ticker, MAX(t.updated_server_time) AS updated_server_time " \
                     f"FROM Candidates c JOIN Tickersdata t ON t.ticker=c.ticker " \
                     f"WHERE c.email='{user.email}' " \
                     f"AND c.enabled = 1 GROUP BY t.ticker) b ON b.ticker=a.ticker " \
                     f"AND b.updated_server_time = a.updated_server_time"
        market_data = db.engine.execute(text(query_text))
        tickers = [dict(r.items()) for r in market_data]
        tickers_arr = [x['ticker'] for x in tickers]
        delim = ","
        prices = current_stock_price_full_w(delim.join(tickers_arr))

        notifications_data = [(x, y) for x in tickers for y in prices if x['ticker'] == y['symbol'] and x['buying_target_price_fmp'] <= y['price']]

        send_email(recipient='support@stockscore.company',
                   subject='StockScore notifications TEST',
                   template='account/email/tickers_notification',
                   data=notifications_data)

    return 'test'


