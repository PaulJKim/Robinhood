from flask import Flask, render_template, request, redirect, Response
from flask_cors import CORS
from Robinhood import Robinhood

import urllib2
import json


app = Flask(__name__)
CORS(app)
rh_client = Robinhood()
logged_in = False

@app.route("/login", methods=['POST'])
def login():
    global logged_in
    content = request.get_json(force=True)
    logged_in = rh_client.login(username=content['user'], password=content['pass'])

    if logged_in:
        message = "Logged in"
    else:
        message = "Failed to log in"

    response = Response(message, status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')

    print logged_in
    return response

@app.route("/logout", methods=['GET'])
def logout():
    global logged_in
    rh_client.logout()

    if logged_in is False:
        return Response("Logging out", status=200, mimetype='application/json')
    else:
        return Response("Not Logged out", status=200, mimetype='application/json')

# Requires paramenter "ticker" ex. fundamentals?ticker=MSFT
@app.route("/fundamentals", methods=['GET'])
def get_fundamentals():
    ticker = request.args.get('ticker')

    # Retrieve fundamentals from Robinhood and convert to JSON
    fundamentals_data = rh_client.get_fundamentals(stock=ticker)

    response = Response(json.dumps(fundamentals_data), status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    print response.get_data()

    return response

# Return JSON list of symbols for securities owned by user
@app.route("/positions", methods=['GET'])
def get_my_positions():
    global logged_in
    if logged_in is True:
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

if __name__ == "__main__":
    app.run()
