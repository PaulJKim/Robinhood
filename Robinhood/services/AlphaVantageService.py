from datetime import datetime, timedelta
from model.TimeSeriesDataPoint import TimeSeriesDataPoint


class AlphaVantageService:

    baseURI = "https://www.alphavantage.co/query?function="
    key = "SVQQFVAXS04D4RUG"

    endpoints = {
        'time_series_intraday': 'TIME_SERIES_INTRADAY&symbol=TICKER&outputsize=full&interval=INTERVAL_LENGTH&apikey=key',
        'time_series_daily': 'TIME_SERIES_DAILY&symbol=TICKER&outputsize=compact&apikey=alphavantage_key',
        'time_series_weekly': 'TIME_SERIES_WEEKLY&symbol=TICKER&apikey=alphavantage_key',
        'time_series_monthly': 'TIME_SERIES_MONTHLY&symbol=TICKER&apikey=alphavantage_key'
    }

    def endpoint(self, time_series_type, ticker):
        return self.baseURI + self.endpoints[time_series_type].replace('TICKER', ticker).replace('alphavantage_key', self.key)

    def set_intraday_interval(self, endpoint, interval):
        try:
            return endpoint.replace('INTERVAL_LENGTH', interval)
        except StandardError as e:
           print "Error: unable to set interval"

    def format_time_series(self, data):
        formatted_dict = {}

        for date, entry in data.iteritems():
            value_dict = {}

            # Remove unnecessary numbering
            for item, value in entry.iteritems():
                item_name_split = item.split(" ")
                value_dict[item_name_split[1]] = value

            formatted_dict[date] = value_dict

        return formatted_dict

    def convert_date(self, date):
        return datetime.strptime(date, "%Y-%m-%d")

    def marshall(self, data):
        time_series_list = list()
        for date, values in data.iteritems():
            volume = values["volume"]
            close = values["close"]
            high = values["high"]
            open = values["open"]
            low = values["low"]
            time_series_list.append(TimeSeriesDataPoint(date, volume, close, high, open, low))

        time_series_list.sort()

        return time_series_list

    def trim_data_intraday(self, entry_list):
        now = datetime.now()
        now_hour = now.hour
        now_minutes = now.minute
        now_seconds = now.second
        trimmed_list_daily = list()

        for entry in entry_list:
            print datetime.strftime(now - timedelta(hours=now_hour, minutes=now_minutes, seconds=now_seconds), "%Y-%m-%d %H:%M:%S")
            if entry.get_date() > datetime.strftime(now - timedelta(hours=now_hour, minutes=now_minutes, seconds=now_seconds), "%Y-%m-%d %H:%M:%S"):
                trimmed_list_daily.append(entry.__dict__)

        return trimmed_list_daily

    def trim_data_daily(self, entry_list):
        now = datetime.now()
        trimmed_list_daily = list()

        for entry in entry_list:
            if entry.get_date() > datetime.strftime(now - timedelta(days=30), "%Y-%m-%d"):
                trimmed_list_daily.append(entry.__dict__)

        return trimmed_list_daily



