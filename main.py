from fastapi import FastAPI
from gridbot_service.gridbot import Gridbot
from endpoints import router as gridbot_router

app = FastAPI()



# Include the gridbot router
app.include_router(gridbot_router, prefix="/bot", tags=["gridbot"])
