import json
import ssl
from urllib.request import urlopen

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)

from flask_login import login_required, current_user

from app import csrf
from app.email import send_email
from app.models import TickerData, Candidate, UserSetting
from app.research.views import research_ticker, get_info_for_ticker

from flask_cors import CORS, cross_origin

candidates = Blueprint('candidates', __name__)


@candidates.route('updatecandidate/', methods=['POST'])
@csrf.exempt
@cross_origin(origin='*',headers=['Content-Type', 'Authorization'])
def updatecandidate():
    c = Candidate()
    c.ticker = request.form['ticker']
    c.reason = request.form['reason']
    c.email = request.form['email']
    c.enabled = True
    fill_ticker_data_from_yahoo(c)
    # return redirect(url_for('candidates.usercandidates'))
    return "success"


@candidates.route('add_by_spider', methods=['POST'])
@csrf.exempt
def add_by_spider():
    ticker_to_add = request.form['ticker_to_add']
    try:
        candidate = Candidate.query.filter_by(email='support@algotrader.company', ticker=ticker_to_add).first()
        if candidate is None:
            print('adding ' + ticker_to_add)
            c = Candidate()
            c.ticker = ticker_to_add
            c.reason = "added automatically"
            c.email = 'support@algotrader.company'
            c.enabled = True
            if not fill_ticker_data_from_yahoo(c):
                print(ticker_to_add + " skept no FMP data...")
                return "skept candidate"
        else:
            return "candidate exist"
    except:
        send_email(recipient='cola.isr@gmail.com',
                   subject='Algotrader adding candidate problem with ' + ticker_to_add,
                   template='account/email/research_issue',
                   ticker=ticker_to_add)
        print("failed to add candidate")
        return "exception in candidate " + ticker_to_add
    # else:
    #     print("skept-exist")
    #     return "skept"


@csrf.exempt
@candidates.route('/info', methods=['GET'])
def info():
    # # Test
    # user = User.query.filter_by(email='liliana.isr@gmail.com').first()
    # send_email(recipient='liliana.isr@gmail.com',
    #            user=user,
    #            subject='Algotrader: Black Swan is suspected!',
    #            template='account/email/black_swan')
    # # End Test

    ticker = request.args['ticker_to_show']
    candidate = Candidate.query.filter_by(ticker=ticker).first()
    m_data = TickerData.query.filter_by(ticker=ticker).order_by(TickerData.updated_server_time.desc()).first()
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()
    td_history = TickerData.query.filter_by(ticker=ticker).order_by(TickerData.updated_server_time.asc()).all()
    hist_dates = []
    hist_algo_ranks = []
    # hist_tr_ranks = []
    # hist_fmp_score = []
    # hist_yahoo_rank = []
    # stock_invest_rank = []
    for td in td_history:
        hist_dates.append(td.updated_server_time.strftime("%d %b, %Y"))
        hist_algo_ranks.append(td.algotrader_rank)
        # hist_tr_ranks.append(td.tipranks)
        # hist_fmp_score.append(td.fmp_score)
        # hist_yahoo_rank.append(td.yahoo_rank)
        # stock_invest_rank.append(td.stock_invest_rank)
    return render_template('candidates/ticker_info.html', user_settings=user_settings,
                           candidate=candidate,
                           market_data=m_data,
                           hist_dates=hist_dates,
                           hist_algo_ranks=hist_algo_ranks)
                           # hist_tr_ranks=hist_tr_ranks,
                           # hist_fmp_score=hist_fmp_score,
                           # hist_yahoo_rank=hist_yahoo_rank,
                           # stock_invest_rank=stock_invest_rank)


@candidates.route('replace_yahoo_data', methods=['POST'])
@csrf.exempt
def replace_yahoo_data():
    ticker_to_add = request.form['ticker_to_add']
    try:
        c = Candidate()
        c.ticker = ticker_to_add
        c.reason = "added automatically"
        c.email = 'support@algotrader.company'
        c.enabled = True
        if not fill_ticker_data_from_yahoo(c):
            print(ticker_to_add + " skept no FMP data...")
            return "skept candidate"
    except:
        print("failed to add candidate")
        return "exception in candidate " + ticker_to_add


def fill_ticker_data_from_yahoo(c):
    candidate_data = get_info_for_ticker(c.ticker)
    if candidate_data is not None:
        c.company_name = candidate_data['longName']
        c.full_description = candidate_data['longBusinessSummary']
        c.exchange = candidate_data['exchange']
        c.industry = candidate_data['industry']
        c.sector = candidate_data['sector']
        c.logo = candidate_data['logo_url']
        c.update_candidate()
        research_ticker(c.ticker)
        return True
    return False

