from database_service.db_operations import (
    get_all_grid_configurations,
    get_grid_configuration_by_id,
    delete_grid_configuration
)
from fastapi import APIRouter, HTTPException

from gridbot_service.gridbot import Gridbot

router = APIRouter()

bot = None  # Initialize bot to None at the module level

@router.post("/gridbot/start")
async def start_bot(config: dict):
    global bot
    bot = Gridbot(config, 'bybit')  # Initialize bot with provided config
    bot.start()
    return {"status": "Bot started successfully"}


@router.post("/stop")
async def stop_bot():
    try:
        bot.stop()
        return {"status": "Bot stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/grid-configurations")
async def list_grid_configurations():
    return get_all_grid_configurations()


@router.get("/grid-configuration/{grid_id}")
async def get_grid_configuration(grid_id: int):
    return get_grid_configuration_by_id(grid_id)


@router.delete("/grid-configuration/{grid_id}")
async def delete_grid_configuration(grid_id: int):
    delete_grid_configuration(grid_id)
    return {"status": "Configuration deleted successfully"}


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
