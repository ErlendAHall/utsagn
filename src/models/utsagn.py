from __future__ import annotations
from typing import TypedDict


class Utsagn:
    source: str
    date_found: str
    speaker: str
    party: str
    utsagn: str


class UtsagnRecordMetadata(TypedDict):
    source: str
    date_found: str
    speaker: str
    party: str


class UtsagnRecord(TypedDict):
    ids: list[str]
    documents: list[str]
    metadatas: list[UtsagnRecordMetadata]
