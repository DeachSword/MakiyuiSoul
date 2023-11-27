import sys
from typing import TYPE_CHECKING, Any, Callable, Dict, Tuple

hoshizora = sys.modules["Makiyui_Hoshizora"]
hoshi = sys.modules["MakiyuiSoulHoshi"]

if TYPE_CHECKING:
    from ....core.setsunano_chikai import SetsunanoChikai, Hoshi as hoshi

    hoshizora = SetsunanoChikai.Hoshizora
HoshiTeraseru = Callable[..., None]

LOGGERS: Dict[str, Tuple[hoshi, HoshiTeraseru]] = {}


class EntityBase(object):
    def __init__(self) -> None:
        pass

    @classmethod
    def get_logger(cls) -> Tuple[hoshi, HoshiTeraseru]:
        name = cls.__name__
        if name not in LOGGERS:
            _hoshizora = hoshizora("DB").Matataku(name)
            LOGGERS[name] = (_hoshizora, _hoshizora.Teraseru)
        return LOGGERS[name]

    @classmethod
    def log(cls, text: Any, **kwargs) -> None:
        _, logger = cls.get_logger()
        logger(text, **kwargs)
