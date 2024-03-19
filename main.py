from fastapi import FastAPI
from controllers import lamoda_controller


app = FastAPI()
app.include_router(lamoda_controller.router)
