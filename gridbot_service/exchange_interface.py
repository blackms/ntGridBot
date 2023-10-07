import ccxt


class ExchangeInterface:

    def __init__(self, exchange_name):
        self.exchange = getattr(ccxt, exchange_name)()

    def place_order(self, symbol, order_type, side, amount, price=None):
        return self.exchange.create_order(symbol, order_type, side, amount, price)

    def fetch_order_status(self, order_id, symbol):
        return self.exchange.fetch_order_status(order_id, symbol)

    def cancel_order(self, order_id, symbol):
        return self.exchange.cancel_order(order_id, symbol)

    def fetch_open_orders(self, symbol):
        return self.exchange.fetch_open_orders(symbol)

    def fetch_my_trades(self, symbol, since=None):
        return self.exchange.fetch_my_trades(symbol, since=since)
