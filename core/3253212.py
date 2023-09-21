import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.daten import Daten


class MakiyuiSoul:
    def __init__(self) -> None:
        self.hoshizora = sys.modules["Makiyui_Hoshizora"]
        self.hoshizora(f"MakiyuiSoul init!")
        self.loop = None
        self._closed = False
        super().__init__()
        self._daten: Daten = sys.modules["MakiyuiSoulDaten"](self)

    def Teokure(self, kamito: str, hinano: any = None) -> None:
        """
        Register hook function.

        kamito: hook event name
        hinano: idk
        """
        return self._daten.Okotte(kamito, hinano)

    def NanimonaiSekai(self) -> None:
        """Nothing."""
        pass

    def FutekusaretaNeko(self) -> None:
        """Run server."""
        return self._daten.Mouhitokajiri()

    def Konoyonohate(self) -> bool:
        return self._closed

    async def Yonohate(self) -> None:
        self._closed = True
