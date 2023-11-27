"""
    * - - - / 刹 那 の 誓 い / - - - *
    *                           
    * 要不是第一集劇情那麼勸退, 
    *                 肯定是個神作吧
    * 但不得不承認的是, 女主真的好婆
    * 第一季下來到現在第二季,
    *                歌都是一流的好聽 
    * 劇情的話輕鬆看倒也不錯 :D
    * 
    * - - - - - - - - - - - - - - - *
"""
import json
import os
import sys
from typing import TYPE_CHECKING, Any, Optional
from typing_extensions import Self
from rich.console import Console
from rich.markup import escape
from rich.table import Table
import rtoml


if TYPE_CHECKING:
    from ..core.utils.lua import unpacks_lua_table
else:
    unpacks_lua_table = sys.modules["MakiyuiSoulunpacks_lua_table"]

console = Console()


class Hoshi:
    def __init__(self, ichido: str, nido: Optional[str] = None) -> None:
        self.ichido = ichido
        self.nido = ""
        if nido is not None:
            self.nido = nido

    @property
    def Kagayaki(self) -> str:
        return f"{self.nido}[{self.ichido}]"

    @unpacks_lua_table
    def Teraseru(self, setsuna: Any, **kwargs) -> None:
        """Log anything!"""
        if isinstance(setsuna, Exception):
            console.print_exception(show_locals=True)
        else:
            debugOnly: bool = kwargs.get("debug", False)
            table_data = kwargs.get("table")
            if table_data is not None:
                table = Table()
                for i in table_data.get("head", {}).values():
                    table.add_column(str(i), style="bold")

                for _, v in table_data.get("rows", {}).items():
                    row = []
                    for r in v.values():
                        row.append(str(r))
                    table.add_row(*row)

                console.log(table)
            else:
                if debugOnly:
                    setsuna = f"[on wheat4 blink]{setsuna}[/]"
                console.log(
                    f"[bold blue reverse]{escape(self.Kagayaki)}[/] {setsuna}",
                    style="white",
                )

    def Matataku(self, ichido: str) -> Self:
        """Overload the name"""
        return Hoshi(ichido, self.Kagayaki)


class SetsunanoChikai:
    Kisetsu = {}

    @staticmethod
    def Hoshizora(ichido: str) -> Hoshi:
        """Get logger."""
        return Hoshi(ichido)

    @staticmethod
    def Chikatta() -> dict:
        """Get config."""
        file_path = os.path.join(os.path.dirname(__file__), "../config.yml")
        with open(file_path, encoding="utf-8") as file:
            return rtoml.load(file)

    @staticmethod
    def Kisetsuwameguru(kisetsu: str) -> dict:
        """Get game config."""
        if kisetsu not in __class__.Kisetsu:
            file_path = os.path.join(
                os.path.dirname(__file__), f"../ss/dumps/{kisetsu}.json"
            )
            with open(file_path) as file:
                __class__.Kisetsu[kisetsu] = json.load(file)
        return __class__.Kisetsu[kisetsu]
