import sys
from typing import TYPE_CHECKING, Dict, Any

_hoshizora = sys.modules["Makiyui_Hoshizora"]("PlayerMgr")
hoshizora = _hoshizora.Teraseru
Warutsu = sys.modules["LibMasquerade!Warutsu"]

if TYPE_CHECKING:
    from ..db.entity.account import Account as GameAccount
    from ..types.TWebSocketServerProtocol import TWebSocketServerProtocol
else:
    GameAccount = sys.modules["GameAccount"]

    TWebSocketServerProtocol = Any


class PlayerMgr:
    def __init__(self) -> None:
        self.__players: Dict[GameAccount, TWebSocketServerProtocol] = {}

    @property
    def players(self):
        return self.__players

    def OnPlayerConnectionLost(self, ws: TWebSocketServerProtocol):
        game_account: GameAccount = getattr(ws, "GameAccount")
        if game_account is not None:
            hoshizora(
                f"[OnPlayerConnectionLost] [red]{game_account.player.nickname}[/]"
            )
            if game_account in self.__players:
                del self.__players[game_account]
            else:
                hoshizora(f"找不到玩家: {self.__players}")

    def OnPlayerLogin(self, player: GameAccount, ws: TWebSocketServerProtocol):
        self.__players[player] = ws

        ## todo: notify for somthing?
