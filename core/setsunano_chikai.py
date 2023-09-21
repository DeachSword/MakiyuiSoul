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
from rich.console import Console
import rtoml


console = Console()

class SetsunanoChikai():
    Kisetsu = {}

    @staticmethod
    def Hoshizora(chikatta: any, **kargs) -> None:
        """Log anything!"""
        console.log(f"{chikatta}")

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
            file_path = os.path.join(os.path.dirname(__file__), f"../ss/dumps/{kisetsu}.json")
            with open(file_path) as file:
                __class__.Kisetsu[kisetsu] = json.load(file)
        return __class__.Kisetsu[kisetsu]