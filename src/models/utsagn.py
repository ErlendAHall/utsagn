from __future__ import annotations
from typing import TypedDict
from pydantic import BaseModel


class Utsagn(BaseModel):
    source: str
    date_found: str
    speaker: str
    party: str
    statement: str


class UtsagnRecordMetadata(TypedDict):
    source: str
    date_found: str
    speaker: str
    party: str


class UtsagnRecord(TypedDict):
    ids: list[str]
    documents: list[str]
    metadatas: list[UtsagnRecordMetadata]
