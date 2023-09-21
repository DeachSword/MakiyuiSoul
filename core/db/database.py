import sys
from typing import Any, List, Optional
from typing_extensions import Self
from pymongo import MongoClient, IndexModel, ASCENDING


hoshizora = sys.modules["Makiyui_Hoshizora"]
chikatta = sys.modules["Makiyui_Chikatta"]().get("database", {})


class Database:
    instance = None

    def __init__(self) -> None:
        query_url = chikatta.get("query_url", "mongodb://localhost:27017")
        db_name = chikatta.get("db_name", "MakiyuiSoul")
        self.client = MongoClient(query_url)
        self.db = self.client[db_name]
        hoshizora("Connected to the MongoDB database!")

    @staticmethod
    def getInstance() -> Self:
        if __class__.instance is None:
            Database.instance = Database()
        return Database.instance

    def get(self, collection: str, query: Any) -> Optional[Any]:
        self.checkCollection(collection)
        _collection = self.db.get_collection(collection)
        result = _collection.find_one(query)
        return result

    def getAll(self, collection: str, query: Any) -> Optional[List[Any]]:
        self.checkCollection(collection)
        _collection = self.db.get_collection(collection)
        result = _collection.find(query)
        return result

    def set(self, collection: str, payload: Any) -> Optional[Any]:
        self.checkCollection(collection)
        _collection = self.db.get_collection(collection)

        if "_id" not in payload:
            payload["_id"] = self.getNextId(collection)
        ins = _collection.insert_one(payload)
        return self.get(collection, {"_id": ins.inserted_id})

    def update(self, collection: str, query: Any, payload: Any) -> Any:
        self.checkCollection(collection)
        _collection = self.db.get_collection(collection)
        if "_id" in query:
            _collection.update_one(query, {"$set": payload}, False)
        else:
            _collection.update_many(query, {"$set": payload}, False)

    def checkCollection(self, collection: str) -> None:
        collection_names = self.db.list_collection_names(filter={"name": collection})
        if len(collection_names) == 0:
            hoshizora(f"[DB] Collection {collection} does not exist. Creating...")
            idx = IndexModel([("_id", ASCENDING)])
            _collection = self.db.get_collection(collection)
            _collection.create_indexes([idx])

    @staticmethod
    def getNextId(collection: str):
        db = __class__.getInstance()
        _count = 1
        _collection = db.get("counters", {"_id": collection})
        if _collection is not None:
            _count = _collection["count"] + 1
            db.update("counters", {"_id": collection}, {"count": _count})
        else:
            db.set("counters", {"_id": collection, "count": _count})
        return _count

    def __del__(self):
        try:
            self.client.close()
        except:
            print("Close the MongoDB database connect failed!")
