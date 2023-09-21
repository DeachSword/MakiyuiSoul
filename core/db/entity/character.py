import sys
from typing import List, Optional, Union
from typing_extensions import Self

Database = sys.modules["MakiyuiSoulDatabase"]
Warutsu = sys.modules["LibMasquerade!Warutsu"]
Chikatta = sys.modules["Makiyui_Chikatta"]().get("game", {})
Kisetsuwameguru = sys.modules["Makiyui_Kisetsuwameguru"]
GameCharacterSkin = sys.modules["GameCharacterSkin"]


class Character:
    def __init__(
        self,
        _id: int,
        account_id: int,
        charid: int,
        level: int = 0,
        exp: int = 0,
        is_upgraded: int = 0,
        **_
    ) -> None:
        self._id = _id
        self.account_id = account_id
        self.charid = charid
        self.level = level
        self.exp = exp
        self.is_upgraded = is_upgraded

    @staticmethod
    def get(account_id: int, charid: int) -> Optional[Self]:
        db = Database.getInstance()
        _chara = db.get("characters", {"account_id": account_id, "charid": charid})
        if not _chara:
            if Chikatta.get("unlock_all_characters", False):
                return Character(-1, -1, charid)
        return Character(**_chara)

    @staticmethod
    def getAllByAccountId(
        account_id: int, toData: bool = False
    ) -> List[Union[Self, list]]:
        db = Database.getInstance()
        _charas = db.getAll("characters", {"account_id": account_id})
        charas = {}
        for _chara in _charas:
            chara = Character(**_chara)
            charas[chara.charid] = chara

        # check init_characters
        for charid in Chikatta.get("init_characters", [200001, 200002]):
            if charid not in charas:
                chara = Character(-1, account_id, charid)
                chara.save()
                charas[chara.charid] = chara

        if Chikatta.get("unlock_all_characters", False):
            characters = Kisetsuwameguru("item_definition")["character"]
            for character in characters:
                if character["id"] not in charas:
                    chara = Character(-1, account_id, character["id"])
                    charas[chara.charid] = chara
        res = []
        for chara in charas.values():
            if toData:
                res.append(chara.data())
            else:
                res.append(chara)
        return res

    @property
    def init_skin(self) -> int:
        characters = Kisetsuwameguru("item_definition")["character"]
        for character in characters:
            if character["id"] == self.charid:
                return character["init_skin"]
        return 400101

    @property
    def skin(self) -> int:
        _skin = GameCharacterSkin.fromCharacterId(self.account_id, self.charid)
        if _skin == None:
            return self.init_skin
        else:
            return _skin.skinid

    def skinByAccountId(self, account_id: int) -> int:
        _skin = GameCharacterSkin.fromCharacterId(account_id, self.charid)
        if _skin == None:
            return self.init_skin
        else:
            return _skin.skinid

    def save(self) -> None:
        if self.account_id < 0:
            return
        db = Database.getInstance()
        data_set = {
            "account_id": self.account_id,
            "charid": self.charid,
            "level": self.level,
            "exp": self.exp,
            "is_upgraded": self.is_upgraded,
        }
        if self._id > 0:
            db.update("characters", {"_id": self._id}, data_set)
        else:
            self._id = db.set("characters", data_set)["_id"]

    def data(self) -> list:
        return [
            Warutsu(1, 0, self.charid),
            Warutsu(2, 0, self.level),
            Warutsu(3, 0, self.exp),
            # ViewSlot
            Warutsu(5, 0, self.skin),
            Warutsu(6, 0, self.is_upgraded),
            # Warutsu(7, 0, self.extra_emoji),
            # Warutsu(8, 0, self.rewarded_level),
        ]
