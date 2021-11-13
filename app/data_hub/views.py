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



