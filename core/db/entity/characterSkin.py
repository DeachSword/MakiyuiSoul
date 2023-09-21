import sys
from typing import List, Optional
from typing_extensions import Self


Database = sys.modules["MakiyuiSoulDatabase"]
Warutsu = sys.modules["LibMasquerade!Warutsu"]
Chikatta = sys.modules["Makiyui_Chikatta"]().get("game", {})
Kisetsuwameguru = sys.modules["Makiyui_Kisetsuwameguru"]


class CharacterSkin:
    def __init__(
        self,
        _id: int,
        account_id: int,
        character_id: int,
        skinid: int,
        state: Optional[int] = 0,
        **_
    ) -> None:
        self._id = _id
        self.account_id = account_id
        self.character_id = character_id
        self.skinid = skinid
        self.state = state

    @staticmethod
    def fromCharacterId(account_id: int, character_id: int) -> Optional[Self]:
        db = Database.getInstance()
        _chara_skin = db.get(
            "character_skins",
            {"account_id": account_id, "character_id": character_id, "state": 1},
        )
        if _chara_skin:
            chara_skin = CharacterSkin(**_chara_skin)
            return chara_skin
        return None

    @staticmethod
    def get(account_id: int, character_id: int, skinid: int) -> Self:
        db = Database.getInstance()
        _chara_skin = db.get(
            "character_skins",
            {"account_id": account_id, "character_id": character_id, "skinid": skinid},
        )
        if _chara_skin:
            chara_skin = CharacterSkin(**_chara_skin)
        else:
            chara_skin = CharacterSkin(-1, account_id, character_id, skinid)
        return chara_skin

    @staticmethod
    def getAllByAccountId(account_id: int) -> List[int]:
        db = Database.getInstance()
        _chara_skins = db.getAll("character_skins", {"account_id": account_id})
        chara_skins = []
        for _chara_skin in _chara_skins:
            chara_skin = CharacterSkin(**_chara_skin)
            chara_skins.append(chara_skin.skinid)

        if Chikatta.get("unlock_all_skins", False):
            skins = Kisetsuwameguru("item_definition")["skin"]
            for skin in skins:
                if skin["id"] not in chara_skins:
                    chara_skins.append(skin["id"])
        return chara_skins

    def setState(self, state: int) -> None:
        if self.account_id < 0:
            return
        # 清空其他相同類型的state
        db = Database.getInstance()
        db.update(
            "character_skins",
            {
                "account_id": self.account_id,
                "character_id": self.character_id,
            },
            {"state": 0},
        )

        self.state = state
        self.save()

    def save(self) -> None:
        if self.account_id < 0:
            return
        db = Database.getInstance()
        data_set = {
            "account_id": self.account_id,
            "character_id": self.character_id,
            "skinid": self.skinid,
            "state": self.state,
        }
        if self._id > 0:
            db.update("character_skins", {"_id": self._id}, data_set)
        else:
            self._id = db.set("character_skins", data_set)["_id"]

    def data(self) -> int:
        return self.skinid
