from fastapi import APIRouter

from gridbot_service.gridbot import Gridbot

router = APIRouter()

# Initialize Gridbot
bot = Gridbot()  # You can pass a default configuration if needed


@router.post("/start")
async def start_bot(config: dict):
    bot.initialize(config)
    bot.start()
    return {"status": "Bot started successfully"}


@router.post("/stop")
async def stop_bot():
    bot.stop()
    return {"status": "Bot stopped successfully"}


@router.get("/status")
async def get_bot_status():
    status = bot.get_status()
    return {"status": status}


@router.post("/config/update")
async def update_config(config: dict):
    bot.update_config(config)
    return {"status": "Configuration updated successfully"}


@router.get("/config")
async def get_config():
    current_config = bot.get_config()
    return {"config": current_config}


@router.get("/active_trades")
async def get_active_trades():
    trades = bot.get_active_trades()
    return {"active_trades": trades}


@router.get("/trade_history")
async def get_trade_history():
    history = bot.get_trade_history()
    return {"trade_history": history}


@router.post("/start_instance")
async def start_instance(config: dict):
    instance_id = bot.start_instance(config)
    return {"status": f"Grid instance {instance_id} started successfully"}


@router.post("/stop_instance/{instance_id}")
async def stop_instance(instance_id: int):
    bot.stop_instance(instance_id)
    return {"status": f"Grid instance {instance_id} stopped successfully"}
