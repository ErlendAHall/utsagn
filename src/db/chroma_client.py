from hashlib import md5
import os
from chromadb import Collection, PersistentClient, QueryResult
from db.seed import seed
from models.utsagn import Utsagn
env = os.getenv("ENV")

class UtsagnDBClient:
    def __init__(self) -> None:

        persistent_path = os.getenv("CHROMA_PERSISTENT_LOCATION")
        if (persistent_path is None) or (persistent_path == ""):
            raise ValueError(
                "CHROMA_PERSISTENT_LOCATION environment variable is not set."
            )
        
        self.chroma_client = PersistentClient(
            path=persistent_path
        )

        self.collection = self.__init_collection()

    def __init_collection(self) -> Collection:
        utsagn_collection = self.chroma_client.get_or_create_collection(
            name="utsagn",
            # https://docs.trychroma.com/docs/embeddings/embedding-functions#default-all-minilm-l6-v2
            # embedding_function=DefaultEmbeddingFunction(),
            metadata={
                "description": "En database med politiske utsagn.",
            },
        )

        return utsagn_collection

    def seed_db(self):
        seed(self.collection)

    def peek(self):
        return self.collection.peek()

    def query_utsagn(self, query_text: list[str] | str) -> QueryResult:
        """
        Perform a query on the utsagn db using textual input.

        :param query_text: The search string. Can be either a single string 
            or a list of strings.
        :type query_text: list[str] | str
        :return: Returns a QueryResult
        :rtype: QueryResult
        """
        return self.collection.query(query_texts=query_text)

    def write_utsagn(self, utsagn: Utsagn) -> bool:
        # Use a md5 digest from the statement and the speaker.
        # Presumably, it is possible that a speaker can perform an identical statement.

        data = utsagn.statement + utsagn.speaker + utsagn.date_found
        id = md5(data.encode("utf-8")).hexdigest()

        try:
            self.collection.upsert(
                ids=[id],
                documents=[utsagn.statement],
                metadatas=[{
                    "date_found": utsagn.date_found,
                    "party": utsagn.party,
                    "source": utsagn.source,
                    "speaker": utsagn.speaker
                }]
            )
            return True

        except:
            return False
