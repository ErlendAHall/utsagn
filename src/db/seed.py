from hashlib import md5
from chromadb import Collection
from models.utsagn import Utsagn, UtsagnRecord, UtsagnRecordMetadata


def utsagn_id(u: Utsagn) -> str:
    """
    Stable id based on the same fields as write_utsagn() in chroma.py.
    """
    data = f'{u["statement"]}{u["speaker"]}{u["date_found"]}'
    return md5(data.encode("utf-8")).hexdigest()


def to_record(utsagn: Utsagn) -> UtsagnRecord:
    ids: list[str] = []
    documents: list[str] = []
    metadatas: list[UtsagnRecordMetadata] = []

    ids.append(utsagn_id(utsagn))
    documents.append(utsagn["statement"])
    metadatas.append(
        {
            "source": utsagn["source"],
            "date_found": utsagn["date_found"],
            "speaker": utsagn["speaker"],
            "party": utsagn.get("party", "") or "",
        }
    )

    return {"ids": ids, "documents": documents, "metadatas": metadatas}


# Entirely fictional test data: names, parties, sources, and quotes are invented.
FICTIONAL_UTSAGN: list[Utsagn] = [
    {
        "date_found": "2025-01-12",
        "party": "Civic Lighthouse Party (CLP)",
        "source": "Harbor City Gazette (fictional)",
        "speaker": "Mara Lindqvist (fictional)",
        "statement": "We will publish every municipal contract in a searchable public ledger within 90 days.",
    },
    {
        "date_found": "2025-02-03",
        "party": "Green Transit Union (GTU)",
        "source": "Northvale Evening Post (fictional)",
        "speaker": "Jonas Kadeem (fictional)",
        "statement": "If elected, I will convert the downtown bus fleet to electric by the end of next year.",
    },
    {
        "date_found": "2025-02-18",
        "party": "Workers & Wires Coalition (WWC)",
        "source": "Metroline Radio Interview (fictional)",
        "speaker": "Elena Sørberg (fictional)",
        "statement": "We will cap broadband prices for low-income households and expand fiber to every neighborhood.",
    },
    {
        "date_found": "2025-03-07",
        "party": "Rural Futures Movement (RFM)",
        "source": "Prairie Standard Weekly (fictional)",
        "speaker": "Caleb Åsheim (fictional)",
        "statement": "I propose a mobile clinic schedule so every village gets primary care at least twice a month.",
    },
    {
        "date_found": "2025-03-21",
        "party": "Education First Alliance (EFA)",
        "source": "Riverbend Tribune (fictional)",
        "speaker": "Sana Holter (fictional)",
        "statement": "We will fund paid apprenticeships for every student who chooses vocational tracks.",
    },
    {
        "date_found": "2025-04-02",
        "party": "Transparent Budget Party (TBP)",
        "source": "City Hall Press Briefing (fictional)",
        "speaker": "Oskar Nyland (fictional)",
        "statement": "Starting this year, we will publish a plain-z budget that shows spending down to each program.",
    },
    {
        "date_found": "2025-04-19",
        "party": "Clean Rivers League (CRL)",
        "source": "Lakeside Herald (fictional)",
        "speaker": "Priya Edevane (fictional)",
        "statement": "We will ban single-use plastics at public events and fund shoreline cleanup crews.",
    },
    {
        "date_found": "2025-05-05",
        "party": "Housing Commons Party (HCP)",
        "source": "Stonebridge Daily (fictional)",
        "speaker": "Noah Vinter (fictional)",
        "statement": "I will introduce a fast-track permit for affordable housing projects that meet energy standards.",
    },
]


def seed(chroma_collection: Collection):
    for utsagn in FICTIONAL_UTSAGN:
        record = to_record(utsagn)
        chroma_collection.upsert(
            ids=record["ids"],
            metadatas=record["metadatas"],
            documents=record["documents"]
        )
