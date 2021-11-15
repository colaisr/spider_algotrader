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
    return result


# http://localhost:8000/data_hub/current_market_operation
@data_hub.route('current_market_operation/', methods=['GET'])
@csrf.exempt
def current_market_operation():
    result=current_market_operation_w()
    return result


# http://localhost:8000/data_hub/current_market_operation
@data_hub.route('current_stock_price_full/<tickers>', methods=['GET'])
@csrf.exempt
def current_stock_price_full(tickers):
    result=current_stock_price_full_w(tickers)
    return result


