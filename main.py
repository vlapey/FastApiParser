from fastapi import FastAPI
from controllers import lamoda_controller, twitch_controller

app = FastAPI()
app.include_router(lamoda_controller.router)
app.include_router(twitch_controller.router)
