from flask import Blueprint, Flask, render_template, request, redirect, Response

import urllib2
import json
from services.AlphaVantageService import AlphaVantageService

alpha_vantage_api = Blueprint('alpha_vantage_api', __name__)
alpha_vantage_service = AlphaVantageService()


@alpha_vantage_api.route("/timeseries/intraday&interval=<interval>/<ticker>", methods=['GET'])
def get_time_series_intraday(interval, ticker):
    """
    Calls Alphavantage API and retrieves daily time series data based on a given interval

    :param interval: Time interval for intraday. Can be 1min, 15min, 30min, 60min
    :param ticker: Stock ticker
    :return: Json payload containing intraday time-series data
    """
    # Reassigned for sake of clarity
    endpoint = alpha_vantage_service.endpoint('time_series_intraday', ticker)
    endpoint = alpha_vantage_service.set_intraday_interval(endpoint, interval)

    try:
        content_raw = urllib2.urlopen(endpoint).read()
        content_json = json.loads(content_raw)
        time_series_data = content_json['Time Series (' + interval + ')']

        # Reformat JSON content by removing numbering from AlphaVantage
        formatted_dict = alpha_vantage_service.format_time_series(time_series_data)

        # Marshall data into time series data point model
        entry_list = alpha_vantage_service.marshall(formatted_dict)

        # Trims daily time series to include only the past 24 hours
        trimmed_entry_list = alpha_vantage_service.trim_data_intraday(entry_list)

        response = Response(json.dumps(trimmed_entry_list), status=200, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response
    except:
        response = Response(status=500, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response


@alpha_vantage_api.route("/timeseries/daily/<ticker>", methods=['GET'])
def get_time_series_daily(ticker):
    """
    Calls Alphavantage API and retrieves daily time series data

    :param ticker: Stock ticker
    :return: Json payload containing daily time-series data
    """
    endpoint = alpha_vantage_service.endpoint('time_series_daily', ticker)

    try:
        content_raw = urllib2.urlopen(endpoint).read()
        content_json = json.loads(content_raw)
        time_series_data = content_json['Time Series (Daily)']

        # Reformat JSON content by removing numbering from AlphaVantage
        formatted_dict = alpha_vantage_service.format_time_series(time_series_data)

        # Marshall data into time series data point model
        entry_list = alpha_vantage_service.marshall(formatted_dict)

        # Trims daily time series to include only the past 4 weeks
        trimmed_entry_list = alpha_vantage_service.trim_data_daily(entry_list)

        response = Response(json.dumps(trimmed_entry_list), status=200, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response
    except:
        response = Response(status=500, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        print (response)
        return response


@alpha_vantage_api.route("/timeseries/weekly/<ticker>", methods=['GET'])
def get_time_series_weekly(ticker):
    """
    Calls Alphavantage API and retrieves weekly time series data

    :param ticker: Stock ticker
    :return: Json payload containing weekly time-series data
    """
    endpoint = alpha_vantage_service.endpoint('time_series_weekly', ticker)

    try:
        content_raw = urllib2.urlopen(endpoint).read()
        content_json = json.loads(content_raw)
        time_series_data = content_json['Weekly Time Series']

        formatted_dict = alpha_vantage_service.format_time_series(time_series_data)

        response = Response(json.dumps(formatted_dict), status=200, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response
    except:
        response = Response(status=500, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response


@alpha_vantage_api.route("/timeseries/monthly/<ticker>", methods=['GET'])
def get_time_series_monthly(ticker):
    """
    Calls Alphavantage API and retrieves monthly time series data

    :param ticker: Stock ticker
    :return: Json payload containing daily time-series data
    """
    endpoint = alpha_vantage_service.endpoint('time_series_monthly', ticker)

    try:
        content_raw = urllib2.urlopen(endpoint).read()
        content_json = json.loads(content_raw)
        time_series_data = content_json['Monthly Time Series']

        formatted_dict = alpha_vantage_service.format_time_series(time_series_data)

        response = Response(json.dumps(formatted_dict), status=200, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response
    except:
        response = Response(status=500, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response
