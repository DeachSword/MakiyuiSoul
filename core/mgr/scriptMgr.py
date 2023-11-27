import glob
import os
import sys
from typing import Optional
import lupa


_hoshizora = sys.modules["Makiyui_Hoshizora"]("ScriptMgr")
hoshizora = _hoshizora.Teraseru


class ScriptMgr:
    def __init__(self) -> None:
        self.lua_runtime = lupa.LuaRuntime(unpack_returned_tuples=True)
        self.scriptMap = {}
        self.loadScripts()

    def loadScripts(self, dir_path: Optional[str] = None) -> None:
        if dir_path is None:
            current_script_path = os.path.abspath(__file__)
            parent_directory = os.path.dirname(os.path.dirname(current_script_path))
            dir_path = os.path.join(parent_directory, "scripts")
        hoshizora(f"Loading scripts... [green]{dir_path}[/]")

        # find lua scripts
        scripts = glob.glob(os.path.join(dir_path, "*.lua"))

        for script in scripts:
            script_name = os.path.basename(script)[:-4]
            with open(script, encoding="utf-8") as f:
                lua_runtime = lupa.LuaRuntime(unpack_returned_tuples=True)
                lua_runtime.execute(f.read())
                lua_runtime.globals().ScriptMgr = self
                lua_runtime.globals().Logger = hoshizora
                self.scriptMap[script_name] = lua_runtime

        hoshizora(f"[green]Success load [red]{len(scripts)}[/] scripts[/]")

    def getScriptInstance(self, script_name: str) -> lupa.LuaRuntime:
        return self.scriptMap[script_name]
