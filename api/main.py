"""
    FastAPI Main
"""
from api.telegram import router as router_telegram
from fastapi import FastAPI

all_routers = (router_telegram,)

app = FastAPI()
for router in all_routers:
    app.include_router(router)
