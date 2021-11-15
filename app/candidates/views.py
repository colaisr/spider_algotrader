import json
from flask import (
    Blueprint,
    request
)

from app import csrf
from app.email import send_email
from app.models import Candidate
from app.research.fmp_wrapper import get_company_info_for_ticker
from app.research.views import research_ticker, get_info_for_ticker

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
        fill_ticker_data_from_fmp(c)
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
        candidate = Candidate.query.filter_by(email='support@algotrader.company', ticker=ticker_to_add).first()
        if candidate is None:
            print('adding ' + ticker_to_add)
            c = Candidate()
            c.ticker = ticker_to_add
            c.reason = "added automatically"
            c.email = 'support@algotrader.company'
            c.enabled = True
            if not fill_ticker_data_from_fmp(c):
                print(ticker_to_add + " skept no FMP data...")
                return "skept candidate"
        else:
            return "candidate exist"
    except:
        send_email(recipient='support@algotrader.company',
                   subject='Algotrader adding candidate problem with ' + ticker_to_add,
                   template='account/email/research_issue',
                   ticker=ticker_to_add,
                   sections="")
        print("failed to add candidate")
        return "exception in candidate " + ticker_to_add
    # else:
    #     print("skept-exist")
    #     return "skept"


def fill_ticker_data_from_fmp(c):
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
        research_ticker(c.ticker)
        return True
    return False

