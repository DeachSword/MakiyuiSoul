import sys
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from core.daten import Daten


class MakiyuiSoul:
    def __init__(self) -> None:
        self._hoshizora = sys.modules["Makiyui_Hoshizora"]("Server")
        self.hoshizora = self._hoshizora.Teraseru
        self.hoshizora("MakiyuiSoul init!")
        self.loop = None
        self._closed = False
        super().__init__()
        self._daten: Daten = sys.modules["MakiyuiSoulDaten"](self)

    def Teokure(self, kamito: str, hinano: Any = None):
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

    @property
    def Konoyonohate(self) -> bool:
        return self._closed

    async def Yonohate(self) -> None:
        self._closed = True
