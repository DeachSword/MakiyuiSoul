from __future__ import annotations
import sys
from typing import TYPE_CHECKING, List, Union


Database = sys.modules["MakiyuiSoulDatabase"]
Warutsu = sys.modules["LibMasquerade!Warutsu"]
Chikatta = sys.modules["Makiyui_Chikatta"]().get("game", {})
Kisetsuwameguru = sys.modules["Makiyui_Kisetsuwameguru"]
GameActivity = sys.modules["GameActivity"]
GameEntityBase = sys.modules["GameEntityBase"]

if TYPE_CHECKING:
    from .gachaRecord import GachaRecord as GameGachaRecord
    from .activity import Activity as GameActivity
    from .entityBase import EntityBase as GameEntityBase
else:
    GameGachaRecord = sys.modules["GameGachaRecord"]


class ActivityGachaUpdateData(GameEntityBase):
    def __init__(self, _id: int, activity_id: int, account_id: int, **_) -> None:
        self._id = _id
        self.activity_id = activity_id
        self.account_id = account_id

    @classmethod
    def getAllByAccountId(
        cls, account_id: int, toData: bool = False
    ) -> List[Union[ActivityGachaUpdateData, list]]:
        # Get all from db
        db = Database.getInstance()
        _aguds = db.getAll("activity_gacha_update_datas", {"account_id": account_id})
        aguds = {}
        for _agud in _aguds:
            agud = ActivityGachaUpdateData(**_agud)
            aguds[agud.activity_id] = agud

        # Active activitys
        activitys = GameActivity.getActiveActivitys("gacha")
        cls.log(f"總共有 {len(activitys)} 個活動", debug=True)
        for activity_id, activity in activitys.items():
            if activity_id not in aguds:
                cls.log(f"找不到活動資料: {activity_id}", debug=True)

                # create init data.
                agud = ActivityGachaUpdateData(-1, activity_id, account_id)
                agud.save()

        # Return ins or bytearray
        res = []
        for agud in aguds.values():
            if toData:
                res.append(agud.data())
            else:
                res.append(agud)
        return res

    @property
    def gained(self) -> List[GameGachaRecord]:
        return []

    @property
    def remain_count(self) -> int:
        # TODO: 總額去減掉gained值
        return 100

    def save(self) -> None:
        db = Database.getInstance()
        data_set = {
            "activity_id": self.activity_id,
            "account_id": self.account_id,
        }
        if self._id > 0:
            db.update("activity_gacha_update_datas", {"_id": self._id}, data_set)
        else:
            self._id = db.set("activity_gacha_update_datas", data_set)["_id"]

    def data(self) -> list:
        res = [
            Warutsu(1, 0, self.activity_id),
            Warutsu(3, 0, self.remain_count),
        ]
        for i in self.gained:
            res.append(Warutsu(2, 2, i.data()))
        return res
