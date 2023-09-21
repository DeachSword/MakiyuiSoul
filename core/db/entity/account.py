import sys
import time
from typing import TYPE_CHECKING, Optional
from typing_extensions import Self
import uuid


Database = sys.modules["MakiyuiSoulDatabase"]
GamePlayer = sys.modules["GamePlayer"]
Warutsu = sys.modules["LibMasquerade!Warutsu"]

if TYPE_CHECKING:
    from .player import Player as GamePlayer


class Account:
    def __init__(
        self,
        _id: int,
        username: str,
        pwd: str,
        has_unread_announcement: int = 0,
        access_token: Optional[str] = None,
        signup_time: Optional[int] = None,
        is_id_card_authed: int = 0,
        country: str = "TW",
        session_id: Optional[str] = None,
    ) -> None:
        self._id = _id
        self.username = username
        self.pwd = pwd
        self.has_unread_announcement = has_unread_announcement
        self._access_token = access_token
        if signup_time is None:
            signup_time = int(time.time())
        self.signup_time = signup_time
        self.is_id_card_authed = is_id_card_authed
        self.country = country
        self.session_id = session_id

        self._player = None

    @staticmethod
    def get(account_id: str) -> Optional[Self]:
        db = Database.getInstance()
        account = db.get("accounts", {"_id": account_id})
        if account is not None:
            return Account(**account)
        return None

    @staticmethod
    def checkUsername(username: str) -> bool:
        db = Database.getInstance()
        account = db.get("accounts", {"username": username})
        if account is not None:
            return True
        return False

    @staticmethod
    def fromLogin(username: str, pwd: str) -> Optional[Self]:
        db = Database.getInstance()
        account = db.get("accounts", {"username": username, "pwd": pwd})
        if account is None:
            return None
        return Account(**account)

    @staticmethod
    def fromOauth2(access_token: str) -> Optional[Self]:
        db = Database.getInstance()
        account = db.get("accounts", {"access_token": access_token})
        if account is None:
            return None
        return Account(**account)

    @staticmethod
    def fromSessionId(session_id: str) -> Optional[Self]:
        db = Database.getInstance()
        account = db.get("accounts", {"session_id": str(session_id)})
        if account is None:
            return None
        return Account(**account)

    @staticmethod
    def create(username: str, pwd: str) -> Self:
        db = Database.getInstance()
        account = db.get("accounts", {"username": username})
        if account:
            raise ValueError(f"Account {username} already exists.")
        new_acc = db.set("accounts", {"username": username, "pwd": pwd})
        return Account(**new_acc)

    @property
    def id(self) -> int:
        return self._id

    @property
    def access_token(self) -> str:
        if self._access_token is not None:
            return self._access_token
        return str(uuid.uuid4())

    @property
    def player(self) -> GamePlayer:
        if self._player is not None:
            return self._player
        return GamePlayer.fromAccountId(self._id)

    def genNewToken(self) -> None:
        self._access_token = str(uuid.uuid4())
        self.save()

    def save(self) -> None:
        db = Database.getInstance()
        data_set = {
            "username": self.username,
            "pwd": self.pwd,
            "has_unread_announcement": self.has_unread_announcement,
            "access_token": self.access_token,
            "signup_time": self.signup_time,
            "is_id_card_authed": self.is_id_card_authed,
            "country": self.country,
            "session_id": self.session_id,
        }
        if self._id > 0:
            db.update("accounts", {"_id": self._id}, data_set)
        else:
            self._id = db.set("accounts", data_set)["_id"]

    def data(self):
        return [
            Warutsu(2, 0, self._id),
            Warutsu(3, 2, self.player.data()),
            Warutsu(5, 0, self.has_unread_announcement),
            Warutsu(6, 2, self.access_token),
            Warutsu(7, 0, self.signup_time),
            Warutsu(8, 0, self.is_id_card_authed),
            Warutsu(9, 2, self.country),
        ]
