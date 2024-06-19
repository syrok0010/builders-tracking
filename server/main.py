from fastapi import FastAPI

from server.builder_info_repository import BuilderInfoRepository
from shared.hardware_info import Builder

app = FastAPI()


@app.post("/init")
async def init(hw: Builder):
    repo = BuilderInfoRepository()
    repo.add_builder(hw)
    return hw


@app.post("/ping/{builder_id}")
async def ping(builder_id: str):
    repo = BuilderInfoRepository()
    repo.update_last_ping(builder_id)
    print('Pinged by ' + builder_id)
    return builder_id
