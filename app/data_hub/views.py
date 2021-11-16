import json
from flask import (
    Blueprint,
    request, jsonify
)

from app import csrf


from flask_cors import cross_origin

from app.research.fmp_wrapper import *

data_hub = Blueprint('data_hub', __name__)


# http://localhost:8000/data_hub/historical_daily_price_full?ticker=msft
@data_hub.route('historical_daily_price_full', methods=['GET'])
@csrf.exempt
def historical_daily_price_full():
    ticker = request.args.get('ticker')
    result=historical_daily_price_full_w(ticker)
    return jsonify(result)


# http://localhost:8000/data_hub/current_market_operation
@data_hub.route('current_market_operation/', methods=['GET'])
@csrf.exempt
def current_market_operation():
    result=current_market_operation_w()
    return jsonify(result)


# http://localhost:8000/data_hub/current_stock_price_full/AAPL,MSFT
@data_hub.route('current_stock_price_full/<tickers>', methods=['GET'])
@csrf.exempt
def current_stock_price_full(tickers):
    result=current_stock_price_full_w(tickers)
    return jsonify(result)

# http://localhost:8000/data_hub/current_stock_price_short/AAPL,MSFT
@data_hub.route('current_stock_price_short/<tickers>', methods=['GET'])
@csrf.exempt
def current_stock_price_short(tickers):
    result=current_stock_price_short_w(tickers)
    return jsonify(result)

# http://localhost:8000/data_hub/stock_news?tickers=AAPL,FB,GOOG,AMZN&limit=50
@data_hub.route('stock_news', methods=['GET'])
@csrf.exempt
def stock_news():
    tickers = request.args.get('tickers')
    limit = request.args.get('limit')
    result=stock_news_w(tickers,limit)
    return jsonify(result)

# http://localhost:8000/data_hub/average_sector_pe_today/Energy
@data_hub.route('average_sector_pe_today/<sector>', methods=['GET'])
@csrf.exempt
def average_pe(sector):
    result=average_sector_pe_today(sector)
    return jsonify(result)

