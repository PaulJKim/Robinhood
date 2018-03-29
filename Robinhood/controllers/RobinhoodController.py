import json
import urllib2

from flask import Blueprint, request, Response

from utils.RobinhoodUtil import RobinhoodUtil

robinhood_api = Blueprint('robinhood_api', __name__)
robinhood_service = RobinhoodUtil()
rh_client = robinhood_service.get_client()

@robinhood_api.route("/login", methods=['POST'])
def login():
    content = request.get_json(force=True)
    robinhood_service.set_logged_in(rh_client.login(username=content['user'], password=content['pass']))
    logged_in = robinhood_service.is_logged_in()

    if logged_in:
        message = "Logged in"
    else:
        message = "Failed to log in"

    response = Response(message, status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')

    print logged_in
    return response


@robinhood_api.route("/logout", methods=['GET'])
def logout():
    req = rh_client.logout()
    print req
    if req.ok:
        return Response("Logging out", status=200, mimetype='application/json')
    else:
        return Response("Not Logged out", status=200, mimetype='application/json')

# Requires paramenter "ticker" ex. fundamentals?ticker=MSFT
@robinhood_api.route("/fundamentals", methods=['GET'])
def get_fundamentals():
    ticker = request.args.get('ticker')

    # Retrieve fundamentals from Robinhood and convert to JSON
    fundamentals_data = rh_client.get_fundamentals(stock=ticker)

    response = Response(json.dumps(fundamentals_data), status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    print response.get_data()

    return response


# Return JSON list of symbols for securities owned by user
@robinhood_api.route("/positions", methods=['GET'])
def get_my_positions():
    if robinhood_service.is_logged_in():
        user_positions = rh_client.securities_owned()['results']
        position_list = list()

        for position in user_positions:
            # Call URL from original dict of positions and then load JSON string and extract symbol for specific stock
            contents = urllib2.urlopen(position['instrument']).read()
            contents_dict = json.loads(contents)
            position_list.append(contents_dict['symbol'])

        response = Response(json.dumps(position_list), status=200, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response
    else:
        response_msg = "Not logged in"
        response = Response(response_msg, status=200, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
