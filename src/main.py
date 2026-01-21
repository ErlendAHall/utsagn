from typing import Union
from fastapi import FastAPI

from db.chroma_client import UtsagnDBClient
from models.utsagn import Utsagn


app = FastAPI()
utsagn_db_client = UtsagnDBClient()


@app.get("/heartbeat")
def read_root():
    return {"Well, hello there"}


@app.get("/utsagn/")
def read_item(query_text: str):
    return utsagn_db_client.query_utsagn(query_text)


@app.post("/utsagn")
def write_item(utsagn: Utsagn):
    return utsagn_db_client.write_utsagn(utsagn)
