import sys
from typing_extensions import Self


Database = sys.modules["MakiyuiSoulDatabase"]
Warutsu = sys.modules["LibMasquerade!Warutsu"]


class AccountLevel:
    def __init__(
        self,
        _id: int,
        account_id: int,
        level_id: int = 0,
        level_type: int = 0,
        score: int = 0,
    ) -> None:
        self._id = _id
        self.account_id = account_id
        self.level_id = level_id
        self.level_type = level_type
        self.score = score

        if self.level_id == 0:
            if self.level_type == 0:
                self.level_id = 10101
            elif self.level_type == 1:
                self.level_id = 20101
            self.save()

    @staticmethod
    def fromAccountId(account_id: int, level_type: int) -> Self:
        db = Database.getInstance()
        _level = db.get(
            "account_levels", {"account_id": account_id, "level_type": level_type}
        )
        if _level:
            return AccountLevel(**_level)
        _level = AccountLevel(-1, account_id, level_type=level_type)
        _level.save()
        return _level

    def save(self) -> None:
        db = Database.getInstance()
        data_set = {
            "account_id": self.account_id,
            "level_id": self.level_id,
            "level_type": self.level_type,
            "score": self.score,
        }
        if self._id > 0:
            db.update("account_levels", {"_id": self._id}, data_set)
        else:
            self._id = db.set("account_levels", data_set)["_id"]

    def data(self) -> list:
        return [
            Warutsu(1, 0, self.level_id),
            Warutsu(2, 0, self.score),
        ]
