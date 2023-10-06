from database_service.db_session import SessionLocal
from database_service.models import GridConfigurations


def create_grid_configuration(trading_pair, grid_range, grid_levels, order_size, order_type, position_type, step,
                              leverage, stop_loss, take_profit):
    session = SessionLocal()
    try:
        new_grid = GridConfigurations(
            trading_pair=trading_pair,
            grid_range=grid_range,
            grid_levels=grid_levels,
            order_size=order_size,
            order_type=order_type,
            position_type=position_type,
            step=step,
            leverage=leverage,
            stop_loss=stop_loss,
            take_profit=take_profit
        )
        session.add(new_grid)
        session.commit()
    except Exception as e:
        print(f"Error creating grid configuration: {e}")
    finally:
        session.close()
