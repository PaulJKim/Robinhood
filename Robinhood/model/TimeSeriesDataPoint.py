class TimeSeriesDataPoint:

    def __init__(self, date, volume, close, high, open, low):
        self.date = date
        self.volume = volume
        self.close_price = close
        self.high_price = high
        self.open_price = open
        self.low_price = low

    def get_date(self):
        return self.date

    def get_volume(self):
        return self.volume

    def get_close(self):
        return self.close_price

    def get_high(self):
        return self.close_price

    def get_open(self):
        return self.close_price

    def get_low(self):
        return self.close_price