from controllers.RobinhoodController import robinhood_api
from flask import Flask
from flask_cors import CORS

from controllers.AlphaVantageController import alpha_vantage_api

app = Flask(__name__)
app.register_blueprint(alpha_vantage_api, url_prefix='/alphavantage')
app.register_blueprint(robinhood_api, url_prefix='/robinhood')

CORS(app)

if __name__ == "__main__":
    app.run()
