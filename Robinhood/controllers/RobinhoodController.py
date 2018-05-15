import json
import urllib2

from flask import Blueprint, request, Response

from utils.RobinhoodUtil import RobinhoodUtil

robinhood_api = Blueprint('robinhood_api', __name__)
robinhood_service = RobinhoodUtil()
rh_client = robinhood_service.get_client()


@robinhood_api.route("/login", methods=['POST'])
def login():
    """
    Login to Robinhood client with credtials

    :return: Reponse with message indicating successful or failed login
    """
    content = request.get_json(force=True)
    robinhood_service.set_logged_in(rh_client.login(username=content['user'], password=content['pass']))
    logged_in = robinhood_service.is_logged_in()

    if logged_in:
        message = "Logged in"
        response = Response(message, status=200, mimetype='application/json')
    else:
        message = "Failed to log in"
        response = Response(message, status=401, mimetype='application/json')

    response.headers.add('Access-Control-Allow-Origin', '*')

    print logged_in
    return response


@robinhood_api.route("/logout", methods=['GET'])
def logout():
    """
    Logout of Robinhood Client

    :return: Response with message indicating successful or failed logout
    """
    req = rh_client.logout()
    print req
    if req.ok:
        return Response("Logging out", status=200, mimetype='application/json')
    else:
        return Response("Not Logged out", status=200, mimetype='application/json')


@robinhood_api.route("/fundamentals", methods=['GET'])
def get_fundamentals():
    """
    Retrieves fundamentals for each owned security for logged in user
    Requires paramenter "ticker" ex. fundamentals?ticker=MSFT

    :return: Response
    """
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
    """
    Retrieves a list of all positions of user in Robinhood

    :return:
    """
    if robinhood_service.is_logged_in():
        user_positions = rh_client.securities_owned()['results']
        position_list = list()

        for position in user_positions:
            # Call URL from original dict of positions and then load JSON string and extract symbol for specific stock
            contents = urllib2.urlopen(position['instrument']).read()
            contents_dict = json.loads(contents)
            position_list.append(contents_dict['symbol'])

        # For Testing
        position_list = ['MSFT', 'SQ', 'W']

        response = Response(json.dumps(position_list), status=200, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response
    else:
        response_msg = "Not logged in"
        response = Response(response_msg, status=401, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

# Return last price of given stock ex. price?ticker=MSFT
@robinhood_api.route("/price", methods=['GET'])
def get_last_price():
    """
    Retrieves last trade price.
    Requires parameter "ticker" ex. price?ticker=MSFT

    :return: Last trade price
    """
    ticker = request.args.get('ticker')

    # Retrieve last trade price from Robinhood
    price = robinhood_service.get_last_trade_price(ticker=ticker)[0][0]

    response = Response(json.dumps(price), status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
