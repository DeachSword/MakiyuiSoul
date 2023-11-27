import sys
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from typing_extensions import Self
from pymongo import MongoClient, IndexModel, ASCENDING
from pymongo.cursor import Cursor


chikatta = sys.modules["Makiyui_Chikatta"]().get("database", {})
hoshizora = sys.modules["Makiyui_Hoshizora"]

if TYPE_CHECKING:
    from ..setsunano_chikai import SetsunanoChikai

    hoshizora = SetsunanoChikai.Hoshizora


class Database:
    instance: Optional[Self] = None

    def __init__(self) -> None:
        self.client = MongoClient(
            chikatta.get("query_url", "mongodb://localhost:27017")
        )
        self.db = self.client[chikatta.get("db_name", "MakiyuiSoul")]
        self._hoshizora = hoshizora("DB")
        self.hoshizora = self._hoshizora.Teraseru
        self.hoshizora("Connected to the MongoDB database!")

        self.__closed = False

    @staticmethod
    def getInstance():
        if Database.instance is None:
            Database.instance = Database()
        return Database.instance

    def get(self, collection: str, query: Any) -> Optional[Any]:
        self.checkCollection(collection)
        _collection = self.db.get_collection(collection)
        result = _collection.find_one(query)
        return result

    def getAll(self, collection: str, query: Any) -> Cursor[Dict[str, Any]]:
        self.checkCollection(collection)
        _collection = self.db.get_collection(collection)
        result: Cursor[Dict[str, Any]]  = _collection.find(query)
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

    def delete(self, collection: str, query: Any) -> None:
        self.checkCollection(collection)
        _collection = self.db.get_collection(collection)
        if "_id" in query:
            _collection.delete_one(query)
        else:
            _collection.delete_many(query)

    def checkCollection(self, collection: str) -> None:
        collection_names = self.db.list_collection_names(filter={"name": collection})
        if len(collection_names) == 0:
            self.hoshizora(f"Collection [bold magenta]{collection}[/] does not exist. Creating...")
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
    
    def close(self):
        if self.__closed:
            return
        try:
            self.hoshizora("Close database...")
            self.client.close()
            self.__closed = True
        except:
            self.hoshizora("[red]Close the MongoDB database connect failed![/red]")

    def __del__(self):
        self.close()