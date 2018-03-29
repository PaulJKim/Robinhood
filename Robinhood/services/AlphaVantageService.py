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
