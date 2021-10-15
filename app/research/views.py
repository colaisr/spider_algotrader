import json

from flask import (
    Blueprint,
    request,
    jsonify
)
from datetime import datetime

from app import csrf
from app.email import send_email
from app.models import TickerData, Candidate, LastUpdateSpyderData, SpiderStatus
from app.models.fgi_score import Fgi_score
from app.research.cnn_fgi_research import get_cnn_fgi_rate
from app.research.tipranks_research import get_tiprank_for_ticker
from app.research.yahoo_research import get_yahoo_stats_for_ticker, get_info_for_ticker, get_complete_graph

from flask_cors import cross_origin

research = Blueprint('research', __name__)


@csrf.exempt
@research.route('/updatefgiscore', methods=['GET'])
def updatefgiscore():
    try:
        fgi_score = Fgi_score()
        val, val_text, updated_cnn = get_cnn_fgi_rate()
        fgi_score.fgi_value = val
        fgi_score.fgi_text = val_text
        fgi_score.score_time = datetime.utcnow()
        fgi_score.updated_cnn = updated_cnn
        fgi_score.add_score()
    except Exception as e:
        print('problem with FGI', e)
    finally:
        return 'Done'


@research.route('updatemarketdataforcandidate/', methods=['POST'])
@csrf.exempt
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def updatemarketdataforcandidate():
    ticker = request.form['ticker_to_update']
    try:
        r = research_ticker(ticker)
    except Exception as e:
        print('problem with research', e)
        return "filed"
    return "success"


@csrf.exempt
@research.route('/updatemarketdataforcandidatespider', methods=['POST'])
def updatemarketdataforcandidatespider():
    ticker = request.form['ticker_to_update']
    try:
        m_data = TickerData.query.filter_by(ticker=ticker).order_by(TickerData.updated_server_time.desc()).first()
        updated = m_data.updated_server_time.date()
        today = datetime.now().date()

        if updated != today:
            result = research_ticker(ticker)
            return result
        else:
            return json.dumps({"status": 0, "sections": []})
        # result, log = research_ticker(ticker)
        # return result, log
    except Exception as e:
        print('problem with research', e)
        return json.dumps({"status": 2, "error": e})


@csrf.exempt
@research.route('/savelasttimeforupdatedata', methods=['POST'])
def savelasttimeforupdatedata():
    error_status = request.form['error_status']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    num_of_positions = request.form['num_of_positions']
    error_tickers = request.form['error_tickers']
    research_error_tickers = request.form['research_error_tickers']
    updated_tickers = request.form['updated_tickers']
    already_updated_tickers = request.form['already_updated_tickers']
    avg_update_times = request.form['avg_update_times']
    error_tickers_num = request.form['error_tickers_num']

    now = datetime.utcnow()
    try:
        last_update_data = LastUpdateSpyderData.query.order_by(LastUpdateSpyderData.start_process_time.desc()).first()
        update_data = LastUpdateSpyderData()
        if error_status == '1':
            update_data.error_status = True
            update_data.error_tickers = error_tickers
            update_data.last_update_date = last_update_data.last_update_date if last_update_data is not None else now
        else:
            update_data.last_update_date = end_time
            update_data.error_status = False
            update_data.error_tickers = '[]'
        update_data.start_process_time = start_time
        update_data.end_process_time = end_time
        update_data.avg_time_by_position = avg_update_times
        update_data.num_of_positions = num_of_positions
        update_data.research_error_tickers = research_error_tickers
        update_data.already_updated_tickers = already_updated_tickers
        update_data.updated_tickers = updated_tickers
        update_data.error_tickers_num = error_tickers_num
        update_data.update_data()
        return "successfully update date"
    except Exception as e:
        print('problem with update last date. ', e)
        return "failed to update date"


@csrf.exempt
@research.route('/update_spider_process_status', methods=['POST'])
def update_spider_process_status():
    status = int(request.form['status'])
    percent = float(request.form['percent'])

    try:
        spider_status = SpiderStatus.query.first()
        if spider_status is None:
            spider_status = SpiderStatus()
        if status == 0:
            spider_status.start_process_date = datetime.utcnow()
            spider_status.status = "spider started"
            spider_status.percent = 0
        elif status == 1:
            spider_status.status = "spider run"
            spider_status.percent = percent
        else:
            spider_status.status = "spider finished"
            spider_status.percent = 100
        spider_status.update_status()
        return "successfully update spider status"
    except Exception as e:
        print('problem with update spider status. ', e)
        return "failed to update spider status"


@csrf.exempt
@research.route('/alltickers', methods=['GET'])  # for use from the task
def alltickers():
    cands = Candidate.query.filter_by(enabled=True).group_by(Candidate.ticker).all()
    resp = []
    for c in cands:
        resp.append(c.ticker)
    return json.dumps(resp)


@csrf.exempt
@research.route('/get_info_ticker/<ticker>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def get_info_ticker(ticker):
    info = get_info_for_ticker(ticker)
    return jsonify(info)


# use ^GSPC for SP500
@csrf.exempt
@research.route('/get_complete_graph_for_ticker/<ticker>', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def get_complete_graph_for_ticker(ticker):
    info = get_complete_graph(ticker)
    info.reset_index(level=0, inplace=True)
    jhistory=info.to_json(orient='records')
    return jsonify(symbol=ticker,historical=jhistory)


def research_ticker(ticker):
    print('started')
    print(datetime.now())
    marketdata = TickerData()
    marketdata.ticker = ticker
    sections = []
    try:
        marketdata.tipranks, marketdata.twelve_month_momentum = get_tiprank_for_ticker(ticker)
    except:
        sections.append("tiprank")
        print("ERROR in MarketDataResearch for " + ticker + ". Section: tiprank")

    try:
        marketdata.yahoo_avdropP, marketdata.yahoo_avspreadP, marketdata.max_intraday_drop_percent = get_yahoo_stats_for_ticker(
            ticker)
    except:
        sections.append("yahooStats")
        print("ERROR in MarketDataResearch for " + ticker + " section: yahooStats")

    try:
        info = get_info_for_ticker(ticker)
        marketdata.beta = info['beta']
        try:
            marketdata.target_mean_price = info['targetMeanPrice']
            difference = marketdata.target_mean_price - info['currentPrice']
            marketdata.under_priced_pnt = round(difference / marketdata.target_mean_price * 100, 1)
            marketdata.yahoo_rank = info['recommendationMean']
        except:
            marketdata.yahoo_rank = None
            marketdata.under_priced_pnt = None
            marketdata.target_mean_price = None
    except:
        sections.append("Yahoo info")
        print("ERROR in Info research for " + ticker + " section: Yahoo info")

    if len(sections) > 0:
        send_email(recipient='support@algotrader.company',
                   subject='Algotrader research problem with ' + ticker,
                   template='account/email/research_issue',
                   ticker=ticker,
                   sections=", ".join(sections))

    ct = datetime.utcnow()

    marketdata.updated_server_time = ct
    marketdata.algotrader_rank = None if marketdata.tipranks == None \
                                         or marketdata.yahoo_rank is None \
                                         or marketdata.yahoo_rank == None \
        else marketdata.tipranks / 2 + 6 - marketdata.yahoo_rank

    marketdata.add_ticker_data()
    error_status = 1 if len(sections) > 0 else 0
    print('ended')
    print(datetime.now())
    return json.dumps({"status": error_status, "sections": sections})
