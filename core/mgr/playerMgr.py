import asyncio
import sys
from typing import TYPE_CHECKING, Dict, Any, List, Optional, Union

_hoshizora = sys.modules["Makiyui_Hoshizora"]("PlayerMgr")
hoshizora = _hoshizora.Teraseru
Warutsu = sys.modules["LibMasquerade!Warutsu"]

if TYPE_CHECKING:
    from ..db.entity.account import Account as GameAccount
    from ..db.entity.activity import Activity as GameActivity
    from ..types.TWebSocketServerProtocol import TWebSocketServerProtocol
    from ...core.utils.lua import unpacks_lua_table
else:
    GameAccount = sys.modules["GameAccount"]
    GameActivity = sys.modules["GameActivity"]
    unpacks_lua_table = sys.modules["MakiyuiSoulunpacks_lua_table"]

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

    @unpacks_lua_table
    def NotifyActivityChange(
        self,
        new_activities: Optional[
            Union[List[GameActivity], Dict[int, GameActivity]]
        ] = None,
        end_activities: Optional[Union[List[int], Dict[int, int]]] = None,
    ):
        NotifyActivityChange = []
        if new_activities:
            for i in new_activities:
                ii = i
                if isinstance(new_activities, dict) and isinstance(i, int):
                    ii = new_activities[i].data()
                elif isinstance(i, GameActivity):
                    ii = i.data()
                else:
                    hoshizora(f"[NotifyActivityChange] Wrong val: [red]{i}[/]")
                    continue
                NotifyActivityChange.append(Warutsu(1, 2, ii))
        if end_activities:
            for i in end_activities:
                ii = i
                if type(end_activities) == dict:
                    ii = end_activities[i]
                NotifyActivityChange.append(Warutsu(2, 0, ii))
        hoshizora(
            f"SEND [red]NotifyActivityChange[/], new_activities: {new_activities}, end_activities: {end_activities}",
            debug=True,
        )
        loop = asyncio.get_running_loop()
        for _, ws in self.players.items():
            loop.create_task(
                ws.RespNotify(".lq.NotifyActivityChange", NotifyActivityChange)
            )
