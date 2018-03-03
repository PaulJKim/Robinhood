from flask import Flask, render_template, request, redirect, Response
from Robinhood import Robinhood

import urllib2
import json


app = Flask(__name__)
rh_client = Robinhood()
logged_in = False

@app.route("/login", methods=['POST'])
def login():
    content = request.get_json(force=True)
    logged_in = rh_client.login(username=content['user'], password=content['pass'])

    if logged_in:
        return "Logged in"
    else:
        return "Failed to log in"

# Requires paramenter "ticker" ex. fundamentals?ticker=MSFT
@app.route("/fundamentals", methods=['GET'])
def get_fundamentals():
    ticker = request.args.get('ticker')

    # Retrieve fundamentals from Robinhood and convert to JSON
    fundamentals_data = rh_client.get_fundamentals(stock=ticker)
    fundamentals_data = json.dumps(fundamentals_data)

    return fundamentals_data

# Return JSON list of symbols for securities owned by user
@app.route("/positions", methods=['GET'])
def get_my_positions():
    user_positions = rh_client.securities_owned()['results']
    position_list = list()

    for position in user_positions:

        # Call URL from original dict of positions and then load JSON string and extract symbol for specific stock
        contents = urllib2.urlopen(position['instrument']).read()
        contents_dict = json.loads(contents)
        position_list.append(contents_dict['symbol'])

    return json.dumps(position_list)

if __name__ == "__main__":
    app.run()
