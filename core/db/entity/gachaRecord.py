import sys
from typing import TYPE_CHECKING


Database = sys.modules["MakiyuiSoulDatabase"]
Warutsu = sys.modules["LibMasquerade!Warutsu"]
Chikatta = sys.modules["Makiyui_Chikatta"]().get("game", {})
Kisetsuwameguru = sys.modules["Makiyui_Kisetsuwameguru"]
hoshizora = sys.modules["Makiyui_Hoshizora"]

if TYPE_CHECKING:
    from ...setsunano_chikai import SetsunanoChikai
    hoshizora = SetsunanoChikai.Hoshizora

class GachaRecord:
    def __init__(
        self,
        _id: int,
        id: int,
        count: int,
        **_
    ) -> None:
        self._id = _id
        self.id = id
        self.count = count

    def data(self) -> list:
        return [
            Warutsu(1, 0, self.id),
            Warutsu(2, 0, self.count),
        ]
