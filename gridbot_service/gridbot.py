import time

import ccxt

from database_service.db_operations import (
    create_grid_configuration,
    create_gridbot_instance
)
from .exchange_interface import ExchangeInterface


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

    def calculate_profit(self, trade, grid_level_price):
        order_price = float(trade['price'])
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
        # Store the grid configuration in the database
        self.grid_id = create_grid_configuration(
            self.config["trading_pair"],
            self.config["grid_range"],
            self.config["grid_levels"],
            self.config["order_size"],
            self.config["order_type"],
            self.config["position_type"],
            self.config["step"],
            self.config["leverage"],
            self.config["stop_loss"],
            self.config["take_profit"]
        )
        # Create a new Gridbot instance in the database
        create_gridbot_instance(self.grid_id, status="active")
        self.running = True
        self.calculate_grid_levels()
        self.place_orders()
        self.monitor_orders()

    def stop(self):
        # Logic to stop the Gridbot
        self.running = False  # You'll need to use this flag in the monitor_orders loop to break out of it

    def update_config(self, new_config: dict):
        # Check if the steps have changed
        if 'step' in new_config and new_config['step'] != self.config['step']:
            # Cancel all remaining orders
            for order in self.active_orders:
                self.exchange.cancel_order(order['id'], self.config['trading_pair'])
            # Update the step in the configuration
            self.config['step'] = new_config['step']
            # Recalculate the grid levels
            self.calculate_grid_levels()
            # Place new orders based on the new grid levels
            self.place_orders()

        # Check if the stop loss has changed
        if 'stop_loss' in new_config:
            self.config['stop_loss'] = new_config['stop_loss']
            # Here, you can add any logic if you need to adjust open positions based on the new stop loss

        # Check if the take profit has changed
        if 'take_profit' in new_config:
            self.config['take_profit'] = new_config['take_profit']
            # Adjust the logic in check_profit_and_restart or any other method that uses take profit

        # Update any other configuration parameters
        for key, value in new_config.items():
            if key not in ['step', 'stop_loss', 'take_profit']:
                self.config[key] = value

    def get_status(self):
        return "Running" if self.running else "Stopped"

    def get_config(self):
        return self.config

    def get_active_trades(self):
        # Assuming the ExchangeInterface has a method to fetch active trades
        return self.exchange.fetch_active_trades(self.config['trading_pair'])

    def get_trade_history(self):
        # Assuming the ExchangeInterface has a method to fetch trade history
        return self.exchange.fetch_trade_history(self.config['trading_pair'])

    def start_instance(self, config: dict):
        # Store the current configuration
        self.config = config
        # Start the bot
        self.start()
        # Assuming the bot instance has an ID, return it
        return self.grid_id

    def stop_instance(self, instance_id: int):
        # For now, we'll assume there's only one instance, so we'll stop the bot
        self.stop()
