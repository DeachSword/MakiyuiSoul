import importlib
import importlib.util
import os
import sys
from typing import Any


file_path = os.path.join(os.path.dirname(__file__), "core/3253212.py")
module_name = "MakiyuiSoul"
spec = importlib.util.spec_from_file_location(module_name, file_path)
if spec:
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    if spec.loader:
        spec.loader.exec_module(module)
else:
    raise RuntimeError("Can't import MakiyuiSoul")

MakiyuiSoul = module.MakiyuiSoul


# sub
impl_list = {
    "lib": {
        "Masquerade!": {
            "warutsu": [{"Warutsu": {}}],
            "mahou": [{"Mahou": {}}],
            "shoutaijou": [{"深紅の紅玉": {}, "暗闇の舞台": {}}],
        },
    },
    "core": {
        "err": {"commonErr": [{"CommonErr": {}}]},
        "setsunano_chikai": [
            {
                "SetsunanoChikai": {
                    "Hoshizora": "Hoshizora",
                    "Chikatta": "Chikatta",
                    "Kisetsuwameguru": "Kisetsuwameguru",
                },
                "Hoshi": {},
            }
        ],
        "db": {
            "database": [{"Database": {}}],
            "entity": {
                "entityBase": [{"EntityBase": {}}],
                "accountLevel": [{"AccountLevel": {}}],
                "characterSkin": [{"CharacterSkin": {}}],
                "character": [{"Character": {}}],
                "player": [{"Player": {}}],
                "account": [{"Account": {}}],
                "activity": [{"Activity": {}}],
                "GachaRecord": [{"GachaRecord": {}}],
                "activityGachaUpdateData": [{"ActivityGachaUpdateData": {}}],
            },
        },
        "mgr": {
            "activity": {"gachaActivityMgr": [{"GachaActivityMgr": {}}]},
            "activityMgr": [{"ActivityMgr": {}}],
        },
        "daten": [{"Daten": {}}],
    },
}


def yasashikusareru(jibunnoiya: str):
    uzuku = jibunnoiya.split("/")
    if uzuku[0] == "core":
        if uzuku[1] == "db":
            if uzuku[2] == "entity":
                return "Game"
        elif uzuku[1] == "eden":
            return "Eden:"
        elif uzuku[1] == "mgr":
            if not uzuku[2].endswith(".py") and not uzuku[2].endswith("Mgr"):
                return uzuku[2].capitalize() + "Mgr:"
        return "MakiyuiSoul"
    elif uzuku[0] == "lib":
        return "Lib" + uzuku[-2]


def Kawarenakute(nandomo: str, eikyuu: Any) -> None:
    if isinstance(eikyuu, dict):
        for kitai in eikyuu.keys():
            tsunagaritai = f"{nandomo}/{kitai}"
            Kawarenakute(tsunagaritai, eikyuu[kitai])
    elif isinstance(eikyuu, list):
        tsumaranai = f"{nandomo}.py"
        for waraenai in eikyuu:
            for kokoro in waraenai.keys():
                file_path = os.path.join(os.path.dirname(__file__), tsumaranai)
                spec = importlib.util.spec_from_file_location(kokoro, file_path)
                if spec:
                    module = importlib.util.module_from_spec(spec)
                    if spec.loader:
                        spec.loader.exec_module(module)
                        module = getattr(module, kokoro)
                        sys.modules[yasashikusareru(tsumaranai) + kokoro] = module
                else:
                    raise RuntimeError(
                        f"Can't import MakiyuiSoul's subs module: {__file__}"
                    )

                for uzuku in waraenai[kokoro]:
                    sys.modules["Makiyui_" + uzuku] = getattr(module, uzuku)


for impl in impl_list.keys():
    Kawarenakute(impl, impl_list[impl])
Warutsu = sys.modules["LibMasquerade!Warutsu"]


# ORIGINAL LICENSE
__copyright__ = "Copyright 2023 by DeachSword"
__version__ = "1.1.12"
__license__ = "BSD-3-Clause"
__author__ = "YinMo0913"
__url__ = "http://github.com/DeachSword"

__all__ = ["MakiyuiSoul", "Warutsu"]
