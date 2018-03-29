from services.Robinhood.Robinhood import Robinhood


class RobinhoodUtil:

    logged_in = False
    rh_client = Robinhood()

    def is_logged_in(self):
        return self.logged_in

    def get_client(self):
        return self.rh_client

    def set_logged_in(self, status):
        self.logged_in = status
