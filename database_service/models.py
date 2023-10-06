from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()


class GridConfigurations(Base):
    __tablename__ = 'grid_configurations'

    id = Column(Integer, primary_key=True)
    trading_pair = Column(String)
    grid_range = Column(String)
    grid_levels = Column(Integer)
    order_size = Column(Float)
    order_type = Column(String)
    position_type = Column(String)
    step = Column(Float)  # Step for each point of the grid
    leverage = Column(Integer, nullable=True)  # Leverage (only for futures)
    stop_loss = Column(Float)  # Stop loss value
    take_profit = Column(Float)  # Take profit value


class ActiveOrders(Base):
    __tablename__ = 'active_orders'

    id = Column(Integer, primary_key=True)
    grid_id = Column(Integer, ForeignKey('grid_configurations.id'))
    order_id = Column(String)
    price = Column(Float)
    size = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    is_future = Column(Boolean, default=False)  # If the pair is a future one
    leverage = Column(Integer, nullable=True)  # Leverage (only for futures)
    pnl = Column(Float)  # Profit and Loss for open grid bot


class TradeHistory(Base):
    __tablename__ = 'trade_history'

    id = Column(Integer, primary_key=True)
    grid_id = Column(Integer, ForeignKey('grid_configurations.id'))
    trade_id = Column(String)
    price = Column(Float)
    size = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    is_future = Column(Boolean, default=False)  # If the pair is a future one
    leverage = Column(Integer, nullable=True)  # Leverage (only for futures)
    pnl = Column(Float)  # Profit and Loss for closed grid bot


class GridbotInstances(Base):
    __tablename__ = 'gridbot_instances'

    id = Column(Integer, primary_key=True)
    grid_id = Column(Integer, ForeignKey('grid_configurations.id'))
    status = Column(String)
    is_active = Column(Boolean, default=True)
