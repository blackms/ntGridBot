import pytest
from database_service.grid_operations import create_grid_configuration
from database_service.db_session import SessionLocal, init_db
from database_service.models import GridConfigurations


# Fixture to set up the test database
@pytest.fixture(scope="module")
def setup_test_db():
    # Initialize the test database and tables
    init_db()
    yield
    # Teardown logic (if needed) can be added here


def test_create_grid_configuration(setup_test_db):
    # Create a sample grid configuration
    trading_pair = "BTC/USDT"
    grid_range = "30000-40000"
    grid_levels = 10
    order_size = 0.1
    order_type = "market"
    position_type = "long"
    step = 1000
    leverage = 10
    stop_loss = 29000
    take_profit = 41000

    create_grid_configuration(trading_pair, grid_range, grid_levels, order_size, order_type, position_type, step,
                              leverage, stop_loss, take_profit)

    # Verify the grid configuration was created in the database
    session = SessionLocal()
    grid = session.query(GridConfigurations).filter_by(trading_pair=trading_pair).first()
    session.close()

    assert grid is not None
    assert grid.trading_pair == trading_pair
    assert grid.grid_range == grid_range
    # ... add more assertions for other fields ...
