from fastapi import FastAPI
from gridbot_service.gridbot import Gridbot

app = FastAPI()

# Initialize the Gridbot (you can also do this dynamically based on API calls)
config_btc_usdt = {
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
btc_usdt_bot = Gridbot(config_btc_usdt, 'bybit')


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/start_gridbot")
async def start_gridbot():
    btc_usdt_bot.start()
    return {"message": "Gridbot started"}


@app.post("/stop_gridbot")
async def stop_gridbot():
    # You'll need to implement a method in the Gridbot class to stop the bot
    btc_usdt_bot.stop()
    return {"message": "Gridbot stopped"}
