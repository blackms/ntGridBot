import pytest
from gridbot_service.gridbot import Gridbot

# Sample configuration for testing
test_config = {
    'trading_pair': 'BTC/USDT',
    'grid_range': '30000-40000',
    'grid_levels': 10,
    'order_size': 0.1,
    'order_type': 'market',
    'position_type': 'long',
    'step': 1000,
    'total_investment': 100,
    'profit_percentage': 10,
    'monitoring_interval': 10
}


def test_gridbot_initialization():
    bot = Gridbot(test_config, 'bybit')
    assert bot.config == test_config
    assert bot.cumulative_profit == 0
    assert bot.active_orders == []


def test_calculate_grid_levels():
    bot = Gridbot(test_config, 'bybit')
    bot.calculate_grid_levels()
    # Assuming the calculate_grid_levels method sets a grid_levels attribute
    assert len(bot.grid_levels) == test_config['grid_levels']


def test_calculate_profit():
    bot = Gridbot(test_config, 'bybit')
    sample_trade = {
        'price': '35000',
        'amount': '0.1'
    }
    grid_level_price = 34000  # This would typically come from your grid levels
    profit = bot.calculate_profit(sample_trade, grid_level_price)

# ... Add more tests for other methods ...
