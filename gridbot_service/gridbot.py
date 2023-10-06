from .exchange_interface import ExchangeInterface
import time
import ccxt

class Gridbot:

    def __init__(self, config, exchange_name):
        self.config = config
        self.exchange = ExchangeInterface(exchange_name)
        self.active_orders = []
        self.cumulative_profit = 0
        self.running = False

    def calculate_grid_levels(self):
        start, end = map(float, self.config['grid_range'].split('-'))
        step = self.config['step']
        self.grid_levels = [start + i * step for i in range(self.config['grid_levels'])]
        self.grid_levels = [price for price in self.grid_levels if price <= end]

    def place_orders(self):
        for price in self.grid_levels:
            order_type = 'buy' if self.config['position_type'] == 'long' else 'sell'
            order = self.exchange.place_order(
                self.config['trading_pair'],
                self.config['order_type'],
                order_type,
                self.config['order_size'],
                price
            )
            self.active_orders.append(order)

    def calculate_profit(self, trade):
        order_price = float(trade['price'])

        if 'grid_level_price' not in self.config:
            raise ValueError("Grid level price is not set in the configuration.")

        grid_level_price = float(self.config['grid_level_price'])
        order_size = float(trade['amount'])
        profit = (order_price - grid_level_price) * order_size
        return profit

    def monitor_orders(self):
        while self.running:
            try:
                open_orders = self.exchange.fetch_open_orders(self.config['trading_pair'])
                recent_trades = self.exchange.fetch_my_trades(self.config['trading_pair'])

                for order in self.active_orders:
                    if order['id'] not in [o['id'] for o in open_orders]:
                        trade = next((t for t in recent_trades if t['order'] == order['id']), None)
                        if trade:
                            self.cumulative_profit += self.calculate_profit(trade)
                            self.check_profit_and_restart()

                time.sleep(self.config.get('monitoring_interval', 10))

            except ccxt.RequestTimeout as e:
                print(f"Request timeout: {e}")
                time.sleep(20)
            except ccxt.ExchangeError as e:
                print(f"Exchange error: {e}")
                time.sleep(20)
            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(20)

    def check_profit_and_restart(self):
        profit_percentage = (self.cumulative_profit / self.config['total_investment']) * 100
        if profit_percentage >= self.config['profit_percentage']:
            self.restart_grid()

    def restart_grid(self):
        for order in self.active_orders:
            self.exchange.cancel_order(order['id'], self.config['trading_pair'])
        self.cumulative_profit = 0
        self.calculate_grid_levels()
        self.place_orders()

    def start(self):
        self.running = True
        self.calculate_grid_levels()
        self.place_orders()
        self.monitor_orders()

    def stop(self):
        # Logic to stop the Gridbot
        self.running = False  # You'll need to use this flag in the monitor_orders loop to break out of it
