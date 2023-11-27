import sys
from typing import TYPE_CHECKING, Any

_hoshizora = sys.modules["Makiyui_Hoshizora"]("GachaActivityMgr")
hoshizora = _hoshizora.Teraseru

if TYPE_CHECKING:
    from ...db.entity.account import Account as GameAccount
    from ...err.commonErr import CommonErr
else:
    GameAccount = sys.modules["GameAccount"]
    CommonErr = sys.modules["MakiyuiSoulCommonErr"]


class GachaActivityMgr:
    def __init__(self) -> None:
        pass

    async def openGacha(self, websocket: Any, activity_id: int, count: int):
        game_account: GameAccount = getattr(websocket, "GameAccount")
        if game_account is not None:
            hoshizora(f"openGacha: {activity_id}, {count}", debug=True)
        raise CommonErr(1000)
