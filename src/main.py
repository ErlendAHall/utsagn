from typing import Union
from fastapi import FastAPI

from db.chroma_client import UtsagnDBClient


app = FastAPI()
utsagn_db_client = UtsagnDBClient()


@app.get("/heartbeat")
def read_root():
    return {"Well, hello there"}


@app.get("/utsagn/query")
def read_item(query_text: str):
    return utsagn_db_client.query_utsagn(query_text)
