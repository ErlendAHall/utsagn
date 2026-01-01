from db.chroma import UtsagnDBClient


def testing():
    client = UtsagnDBClient()
    client.seed_db()
    return client.peek()


print(testing())
