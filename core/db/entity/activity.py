from __future__ import annotations
import sys
from time import time
from typing import TYPE_CHECKING, Dict, List, Optional, Union


Database = sys.modules["MakiyuiSoulDatabase"]
Warutsu = sys.modules["LibMasquerade!Warutsu"]
Chikatta = sys.modules["Makiyui_Chikatta"]().get("game", {})
Kisetsuwameguru = sys.modules["Makiyui_Kisetsuwameguru"]
GameEntityBase = sys.modules["GameEntityBase"]

if TYPE_CHECKING:
    from .entityBase import EntityBase as GameEntityBase


class Activity(GameEntityBase):
    def __init__(
        self,
        _id: int,
        activity_id: int,
        start_time: int,
        end_time: int,
        _type: str,
        **_,
    ) -> None:
        self._id = _id
        self.activity_id = activity_id
        self.start_time = start_time
        self.end_time = end_time
        self._type = _type
    
    @property
    def is_active(self):
        now_time = time()
        return now_time >= self.start_time and now_time < self.end_time

    @classmethod
    def getAll(cls, toData: bool = False, activeOnly: bool = True) -> List[Union[Activity, list]]:
        activitys = []
        if Chikatta.get("unlock_all_activitys", False):
            _activitys = Kisetsuwameguru("activity")["activity"]
            for _activity in _activitys:
                activity = Activity(-1, _activity["id"], 0, 99999999, _activity["type"])
                if toData:
                    activitys.append(activity.data())
                else:
                    activitys.append(activity)
            return activitys

        if activeOnly:
            _activitys = cls.getActiveActivitys()
            if _activitys:
                for _, activity in _activitys.items():
                    if toData:
                        activitys.append(activity.data())
                    else:
                        activitys.append(activity)
        else:
            db = Database.getInstance()
            _activitys = db.getAll("activitys", {})
            if _activitys:
                for _activity in _activitys:
                    activity = Activity(**_activity)
                    if toData:
                        activitys.append(activity.data())
                    else:
                        activitys.append(activity)
        return activitys

    @staticmethod
    def getActiveActivitys(activity_type: Optional[str] = None) -> Dict[int, Activity]:
        activitys: Dict[int, Activity] = {}
        activity_types: Dict[int, str] = {}

        # 先獲取類型
        _activitys = Kisetsuwameguru("activity")["activity"]
        for _activity in _activitys:
            activity_types[_activity["id"]] = _activity["type"]

        # Get all active activities.
        db = Database.getInstance()
        now_time = time()
        __class__.log(f"now_time: {now_time}", debug=True)
        _activitys = db.getAll(
            "activitys",
            {"start_time": {"$lte": now_time}, "end_time": {"$gt": now_time}},
        )
        if _activitys:
            for _activity in _activitys:
                activity = Activity(**_activity)
                if activity.activity_id in activity_types:
                    if activity_type is None or activity_type == activity_types[activity.activity_id]:
                        activitys[activity.activity_id] = activity
        return activitys

    @staticmethod
    def get(activity_id: int) -> Optional[Activity]:
        db = Database.getInstance()
        _activity = db.get("activitys", {"activity_id": activity_id})
        if _activity:
            activity = Activity(**_activity)
            return activity
        return None

    @staticmethod
    def initActivitys() -> None:
        add_activitys = Chikatta.get("add_activitys", [])
        if add_activitys:
            now_all: Dict[int, Activity] = {}
            for i in __class__.getAll(activeOnly=False):
                if isinstance(i, Activity):
                    now_all[i.activity_id] = i
            for ii in add_activitys:
                if ii["activity_id"] not in now_all:
                    activity = Activity(
                        -1,
                        ii["activity_id"],
                        ii["start_time"],
                        ii["end_time"],
                        ii["_type"],
                    )
                    activity.save()
                    now_all[activity.activity_id] = activity
                    __class__.log(f"Add new activity: {activity.activity_id}")
                else:
                    activity = now_all[ii["activity_id"]]
                    if (
                        ii["start_time"] != activity.start_time
                        or ii["end_time"] != activity.end_time
                        or ii["_type"] != activity._type
                    ):
                        activity.start_time = ii["start_time"]
                        activity.end_time = ii["end_time"]
                        activity._type = ii["_type"]
                        activity.save()
                        __class__.log(f"Update activity: {activity.activity_id}")

    def save(self) -> None:
        db = Database.getInstance()
        data_set = {
            "activity_id": self.activity_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "_type": self._type,
        }
        if self._id > 0:
            db.update("activitys", {"_id": self._id}, data_set)
        else:
            self._id = db.set("activitys", data_set)["_id"]

    def delete(self) -> None:
        db = Database.getInstance()
        db.delete("activitys", {"_id": self._id})

    def data(self) -> list:
        return [
            Warutsu(1, 0, self.activity_id),
            Warutsu(2, 0, self.start_time),
            Warutsu(3, 0, self.end_time),
            Warutsu(4, 2, self._type),
        ]
