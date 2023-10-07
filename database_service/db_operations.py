from .db_session import SessionLocal
from .models import GridConfigurations, GridbotInstances, TradeHistory, ActiveOrders


def create_grid_configuration(trading_pair, grid_range, grid_levels, order_size, order_type, position_type, step,
                              leverage, stop_loss, take_profit):
    session = SessionLocal()
    grid_config = GridConfigurations(
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
    session.add(grid_config)
    session.commit()
    grid_id = grid_config.id
    session.close()
    return grid_id


def log_active_trade(grid_id, order_id, price, size, is_future, leverage, pnl):
    session = SessionLocal()
    active_trade = ActiveOrders(
        grid_id=grid_id,
        order_id=order_id,
        price=price,
        size=size,
        is_future=is_future,
        leverage=leverage,
        pnl=pnl
    )
    session.add(active_trade)
    session.commit()
    session.close()


def close_active_trade(order_id, trade_id, price, size, pnl):
    session = SessionLocal()
    active_trade = session.query(ActiveOrders).filter_by(order_id=order_id).first()

    if not active_trade:
        session.close()
        raise ValueError(f"No active trade found with order_id {order_id}")

    trade_history = TradeHistory(
        grid_id=active_trade.grid_id,
        trade_id=trade_id,
        price=price,
        size=size,
        is_future=active_trade.is_future,
        leverage=active_trade.leverage,
        pnl=pnl
    )
    session.add(trade_history)
    session.delete(active_trade)
    session.commit()
    session.close()


def create_gridbot_instance(grid_id, status):
    session = SessionLocal()
    gridbot_instance = GridbotInstances(
        grid_id=grid_id,
        status=status
    )
    session.add(gridbot_instance)
    session.commit()
    session.close()


def update_gridbot_instance_status(instance_id, new_status):
    session = SessionLocal()
    gridbot_instance = session.query(GridbotInstances).filter_by(id=instance_id).first()

    if not gridbot_instance:
        session.close()
        raise ValueError(f"No gridbot instance found with id {instance_id}")

    gridbot_instance.status = new_status
    session.commit()
    session.close()


def get_all_grid_configurations():
    session = SessionLocal()
    grid_configs = session.query(GridConfigurations).all()
    session.close()
    return grid_configs


def get_grid_configuration_by_id(grid_id: int):
    session = SessionLocal()
    grid_config = session.query(GridConfigurations).filter_by(id=grid_id).first()
    session.close()
    if not grid_config:
        raise ValueError(f"No grid configuration found with id {grid_id}")
    return grid_config


def delete_grid_configuration(grid_id: int):
    session = SessionLocal()
    grid_config = session.query(GridConfigurations).filter_by(id=grid_id).first()
    if not grid_config:
        session.close()
        raise ValueError(f"No grid configuration found with id {grid_id}")
    session.delete(grid_config)
    session.commit()
    session.close()
