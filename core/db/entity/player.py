import sys
from typing import TYPE_CHECKING, List, Optional, Union
from typing_extensions import Self


Database = sys.modules["MakiyuiSoulDatabase"]
Warutsu = sys.modules["LibMasquerade!Warutsu"]
Kisetsuwameguru = sys.modules["Makiyui_Kisetsuwameguru"]
Chikatta = sys.modules["Makiyui_Chikatta"]().get("game", {})
GameAccountLevel = sys.modules["GameAccountLevel"]
GameCharacter = sys.modules["GameCharacter"]
GameCharacterSkin = sys.modules["GameCharacterSkin"]

if TYPE_CHECKING:
    from .accountLevel import AccountLevel as GameAccountLevel
    from .character import Character as GameCharacter


class Player:
    def __init__(
        self,
        _id: int,
        account_id: int,
        nickname: str = "BAO",
        login_time: int = 0,
        logout_time: int = 0,
        room_id: int = 0,
        title: int = 0,
        signature: str = "",
        email: str = "",
        email_verify: int = 0,
        gold: int = 0,
        diamond: int = 0,
        vip: int = 0,
        birthday: int = 0,
        phone: str = "",
        phone_verify: int = 0,
        avatar_frame: int = 0,
        skin_ticket: int = 0,
        verified: int = 0,
        frozen_state: int = 0,
        character_id: Optional[int] = None,
        **_
    ) -> None:
        self._id = _id
        self.account_id = account_id
        self.nickname = nickname
        self.login_time = login_time
        self.logout_time = logout_time
        self.room_id = room_id
        ## self.anti_addiction = anti_addiction
        self.title = title
        self.signature = signature
        self.email = email
        self.email_verify = email_verify
        self.gold = gold
        self.diamond = diamond
        self.vip = vip
        self.birthday = birthday
        self.phone = phone
        self.phone_verify = phone_verify
        # self.platform_diamond = platform_diamond
        ## self.level = level
        ## self.level3 = level3
        self.avatar_frame = avatar_frame
        self.skin_ticket = skin_ticket
        # self.platform_skin_ticket = platform_skin_ticket
        self.verified = verified
        # self.challenge_levels = challenge_levels
        # self.achievement_count = achievement_count
        self.avatar_frame = avatar_frame
        self.frozen_state = frozen_state
        # self.loading_image = loading_image

        if character_id is None:
            self.character_id = Chikatta.get("init_character_id", 200001)
        else:
            self.character_id = character_id

    @staticmethod
    def fromAccountId(account_id: int) -> Self:
        db = Database.getInstance()
        _player = db.get("players", {"account_id": account_id})
        if _player:
            return Player(**_player)
        _player = Player(-1, account_id)
        _player.save()
        return _player

    @property
    def level(self) -> GameAccountLevel:
        return GameAccountLevel.fromAccountId(self.account_id, 0)

    @property
    def level3(self) -> GameAccountLevel:
        return GameAccountLevel.fromAccountId(self.account_id, 1)

    @property
    def character(self) -> GameCharacter:
        return GameCharacter.get(self.account_id, self.character_id)

    @property
    def avatar_id(self) -> int:
        return self.character.skinByAccountId(self.account_id)

    def getCharacters(self, toData: bool = False) -> List[GameCharacter]:
        characters = GameCharacter.getAllByAccountId(self.account_id, toData)
        return characters

    def getCharacterSkins(self) -> List[int]:
        skinIds = GameCharacterSkin.getAllByAccountId(self.account_id)
        return skinIds

    def changeMainCharacter(self, character_id: int) -> int:
        _chara = GameCharacter.get(self.account_id, character_id)
        if _chara or Chikatta.get("unlock_all_characters", False):
            characters = Kisetsuwameguru("item_definition")["character"]
            for character in characters:
                if character["id"] == character_id:
                    self.character_id = character_id
                    self.save()
                    return -1
        return 1007

    def changeCharacterSkin(self, character_id: int, skin_id: int) -> int:
        _chara = GameCharacter.get(self.account_id, character_id)
        if _chara or Chikatta.get("unlock_all_characters", False):
            skins = Kisetsuwameguru("item_definition")["skin"]
            for skin in skins:
                if skin["id"] == skin_id and skin["character_id"] == character_id:
                    chara_skin = GameCharacterSkin.get(
                        self.account_id, character_id, skin_id
                    )
                    chara_skin.setState(1)
                    return -1
        return 1007

    def save(self) -> None:
        db = Database.getInstance()
        data_set = {
            "account_id": self.account_id,
            "nickname": self.nickname,
            "login_time": self.login_time,
            "logout_time": self.logout_time,
            "room_id": self.room_id,
            "title": self.title,
            "signature": self.signature,
            "email": self.email,
            "email_verify": self.email_verify,
            "gold": self.gold,
            "diamond": self.diamond,
            "vip": self.vip,
            "birthday": self.birthday,
            "phone": self.phone,
            "phone_verify": self.phone_verify,
            "avatar_frame": self.avatar_frame,
            "skin_ticket": self.skin_ticket,
            "verified": self.verified,
            "frozen_state": self.frozen_state,
            "character_id": self.character_id,
        }
        if self._id > 0:
            db.update("players", {"_id": self._id}, data_set)
        else:
            self._id = db.set("players", data_set)["_id"]

    def baseView(self) -> list:
        return [
            Warutsu(1, 0, self.account_id),
            Warutsu(2, 0, self.avatar_id),
            Warutsu(3, 0, self.title),
            Warutsu(4, 2, self.nickname),
            Warutsu(5, 2, self.level.data()),
            Warutsu(6, 2, self.level3.data()),
            Warutsu(7, 0, self.avatar_frame),
            Warutsu(8, 0, self.verified),
            Warutsu(9, 0, 0),  # is_banned
        ]

    def gameView(self) -> list:
        return [
            Warutsu(1, 0, self.account_id),
            Warutsu(2, 0, self.avatar_id),
            Warutsu(3, 0, self.title),
            Warutsu(4, 2, self.nickname),
            Warutsu(5, 2, self.level.data()),
            Warutsu(6, 2, self.character.data()),
            Warutsu(7, 2, self.level3.data()),
            Warutsu(8, 0, self.avatar_frame),
            Warutsu(9, 0, self.verified),
        ]

    def data(self) -> list:
        return [
            Warutsu(1, 0, self.account_id),
            Warutsu(2, 2, self.nickname),
            Warutsu(3, 0, self.login_time),
            Warutsu(4, 0, self.logout_time),
            Warutsu(5, 0, self.room_id),
            Warutsu(7, 0, self.title),
            Warutsu(8, 2, self.signature),
            Warutsu(9, 2, self.email),
            Warutsu(10, 0, self.email_verify),
            Warutsu(11, 0, self.gold),
            Warutsu(12, 0, self.diamond),
            Warutsu(13, 0, self.avatar_id),
            Warutsu(14, 0, self.vip),
            Warutsu(15, 0, self.birthday),
            Warutsu(16, 2, self.phone),
            Warutsu(17, 0, self.phone_verify),
            Warutsu(21, 2, self.level.data()),
            Warutsu(22, 2, self.level3.data()),
            Warutsu(23, 0, self.avatar_frame),
            Warutsu(24, 0, self.skin_ticket),
            Warutsu(26, 0, self.verified),
            Warutsu(29, 0, self.frozen_state),
        ]
