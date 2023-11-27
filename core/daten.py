import asyncio
from functools import wraps
import sys
import time
import websockets
from websockets import WebSocketServerProtocol, serve
from websockets.exceptions import ConnectionClosedError
from prompt_toolkit.shortcuts import PromptSession
from typing import TYPE_CHECKING, Any, Optional


chikatta = sys.modules["Makiyui_Chikatta"]().get("daten", {})
odori = sys.modules["LibMasquerade!Mahou"]
rubii = sys.modules["LibMasquerade!深紅の紅玉"]
suteeji = sys.modules["LibMasquerade!暗闇の舞台"]
Warutsu = sys.modules["LibMasquerade!Warutsu"]

if TYPE_CHECKING:
    from .db.database import Database
    from .db.entity.account import Account as GameAccount
    from .db.entity.activity import Activity as GameActivity
    from .mgr.playerMgr import PlayerMgr
    from .mgr.activityMgr import ActivityMgr
    from .mgr.scriptMgr import ScriptMgr
    from .err.commonErr import CommonErr
    from .types.TWebSocketServerProtocol import TWebSocketServerProtocol

    MakiyuiSoul = Any
else:
    MakiyuiSoul = sys.modules["MakiyuiSoul"]
    Database = sys.modules["MakiyuiSoulDatabase"]
    GameAccount = sys.modules["GameAccount"]
    GameActivity = sys.modules["GameActivity"]
    GameActivityGachaUpdateData = sys.modules["GameActivityGachaUpdateData"]
    PlayerMgr = sys.modules["MakiyuiSoulPlayerMgr"]
    ActivityMgr = sys.modules["MakiyuiSoulActivityMgr"]
    ScriptMgr = sys.modules["MakiyuiSoulScriptMgr"]
    CommonErr = sys.modules["MakiyuiSoulCommonErr"]
    TWebSocketServerProtocol = Any


class Daten:
    def __init__(self, soul: MakiyuiSoul) -> None:
        self._soul = soul
        self._falling = {}
        self._readline: Optional[asyncio.Task] = None
        self.hoshizora(f"Daten init!")

        # 實例
        self.playerMgr = PlayerMgr()
        self.activityMgr = ActivityMgr()
        self.scriptMgr = ScriptMgr()

        # state
        self.__state = asyncio.Future()

    @property
    def hoshizora(self):
        return self._soul.hoshizora

    @property
    def black_out(self) -> bool:
        return self._soul.Konoyonohate

    async def Dokomademo(self, websocket: WebSocketServerProtocol, path: str):
        websocket = suteeji.__init__(websocket)
        try:
            async for message in websocket:
                rpcName, rpcData, reqIdx = await odori.decodeData(message)
                await self.Kyoukaisen(rpcName, rpcData, reqIdx, websocket)
            self.playerMgr.OnPlayerConnectionLost(websocket)
        except ConnectionClosedError as e:
            self.playerMgr.OnPlayerConnectionLost(websocket)

    def Mouhitokajiri(self) -> None:
        async def runner():
            async with self:
                self.__state = asyncio.Future()
                host_addr = chikatta.get("host_addr", "localhost")
                host_port = chikatta.get("host_port", 8765)
                async with serve(
                    self.Dokomademo, host_addr, host_port, compression=None
                ):
                    self.hoshizora(f"Server host on {host_addr}:{host_port}")
                    self._readline = asyncio.create_task(self.readline())
                    await self.__state
                self.hoshizora(f"[red]Server Down[/]")

        try:
            asyncio.run(runner())
        except KeyboardInterrupt:
            return

    async def Kyoukaisen(
        self,
        rpcName: str,
        rpcData: str,
        reqIdx: int,
        websocket: WebSocketServerProtocol,
    ) -> None:
        """Callback to handler."""
        if rpcName in self._falling:
            await self._falling[rpcName](websocket, rpcData, reqIdx)
        else:
            await self.Kyouhan(rpcName, rpcData, reqIdx, websocket)

    async def Kyouhan(
        self,
        rpcName: str,
        rpcData: dict,
        reqIdx: int,
        websocket: TWebSocketServerProtocol,
    ) -> None:
        """Handle some time."""
        _rpc_hoshizora = self._soul._hoshizora.Matataku("RPC")
        rpc_hoshizora = _rpc_hoshizora.Teraseru
        lobby_hoshizora = _rpc_hoshizora.Matataku("LOBBY").Teraseru
        fast_hoshizora = _rpc_hoshizora.Matataku("FAST").Teraseru
        try:
            if rpcName == ".lq.Lobby.login":
                username = rpcData[1]
                pwd = rpcData[2]
                if GameAccount.checkUsername(username):
                    account = GameAccount.fromLogin(username, pwd)
                    if account is None:
                        return await websocket.RespErr(reqIdx, 1003, 1)  # 密碼錯誤
                    else:
                        account.genNewToken()
                        setattr(websocket, "GameAccount", account)
                        self.playerMgr.OnPlayerLogin(account, websocket)
                        return await websocket.RespCommon(reqIdx, account.data())
                else:
                    if chikatta.get("auto_create_account", False):
                        # create account
                        account = GameAccount.create(username, pwd)
                        setattr(websocket, "GameAccount", account)
                        return await websocket.RespCommon(reqIdx, account.data())
                    else:
                        return await websocket.RespErr(reqIdx, 1002, 1)
            elif rpcName == ".lq.Lobby.signup":
                return await websocket.RespErr(reqIdx, 1003, 1)
            elif rpcName == ".lq.Lobby.oauth2Check":
                access_token = rpcData[2]
                account = GameAccount.fromOauth2(access_token)
                if account:
                    return await websocket.RespCommon(reqIdx, Warutsu(2, 0, 1))
                return await websocket.RespErr(reqIdx, 109, 1)
            elif rpcName == ".lq.Lobby.oauth2Login":
                access_token = rpcData[2]
                account = GameAccount.fromOauth2(access_token)
                if account:
                    setattr(websocket, "GameAccount", account)
                    self.playerMgr.OnPlayerLogin(account, websocket)
                    return await websocket.RespCommon(reqIdx, account.data())
                return await websocket.RespErr(reqIdx, 109, 1)
            elif rpcName == ".lq.Lobby.fetchServerTime":
                ResServerTime = [Warutsu(1, 0, int(time.time()))]
                return await websocket.RespCommon(reqIdx, ResServerTime)
            elif rpcName == ".lq.Lobby.fetchCharacterInfo":
                account = getattr(websocket, "GameAccount")
                if account is not None:
                    player = account.player
                    ResCharacterInfo = [
                        Warutsu(4, 0, player.character_id),
                    ]
                    for character in player.getCharacters(True):
                        ResCharacterInfo.append(Warutsu(2, 2, character))
                    for skinId in player.getCharacterSkins():
                        ResCharacterInfo.append(Warutsu(3, 0, skinId))
                    return await websocket.RespCommon(reqIdx, ResCharacterInfo)
                return await websocket.RespErr(reqIdx, 1002, 1)
            elif rpcName == ".lq.Lobby.changeMainCharacter":
                character_id = rpcData[1]
                account: GameAccount = getattr(websocket, "GameAccount")
                if account is not None:
                    errCode = account.player.changeMainCharacter(character_id)
                    if errCode > 0:
                        return await websocket.RespErr(reqIdx, errCode, 1)
                else:
                    return await websocket.RespErr(reqIdx, 1002, 1)
            elif rpcName == ".lq.Lobby.changeCharacterSkin":
                character_id = rpcData[1]
                skin = rpcData[2]
                account = getattr(websocket, "GameAccount")
                if account is not None:
                    errCode = account.player.changeCharacterSkin(character_id, skin)
                    if errCode > 0:
                        return await websocket.RespErr(reqIdx, errCode, 1)
                else:
                    return await websocket.RespErr(reqIdx, 1002, 1)
            else:
                rpc_hoshizora(
                    f"no handle on [red]{rpcName}[/], payload: [green]{rpcData}[/]"
                )
                return await websocket.RespCommon(reqIdx)
        except CommonErr as e:
            return await websocket.RespErr(reqIdx, e.code, e.fid)
        except Exception as e:
            rpc_hoshizora(e)

    def Okotte(self, kamito: str, hinano: any = None) -> None:
        def decorator(func):
            @wraps(func)
            async def __check(*args):
                await func(*args)

            self._falling[kamito] = __check

        return decorator

    async def readline(self) -> None:
        session = PromptSession("> ")
        _cmd_hoshizora = self._soul._hoshizora.Matataku("CMD")
        cmd_hoshizora = _cmd_hoshizora.Teraseru

        def init_state(x):
            x.globals().self = self
            x.globals()._cmd_hoshizora = _cmd_hoshizora
            x.globals().cmd_hoshizora = cmd_hoshizora
            x.globals().VarState.state = True
            x.globals().pexec = exec
            x.globals().GameActivity = GameActivity
            return x

        script_ins = self.scriptMgr.getScriptInstance("readline_handler")
        readline_handler = init_state(script_ins)
        OnCmd = readline_handler.globals().OnCmd
        forceJump = False
        while readline_handler.globals().VarState.state:
            if script_ins.globals().VarState.ins is not None:
                script_ins = script_ins.globals().VarState.ins
                readline_handler = init_state(script_ins)
                OnCmd = readline_handler.globals().OnCmd
                cmd_hoshizora("Reload success!")
                continue
            try:
                result: str = await session.prompt_async()
                OnCmd(result)

                # close the door
                forceJump = False
            except KeyboardInterrupt:
                cmd_hoshizora(f"Use `exit` to close server")

                # exit door
                if forceJump:
                    break
                forceJump = True
            except Exception as e:
                cmd_hoshizora(e)
        cmd_hoshizora(f"Quit readline and close server...")
        await self.Yonohate()

    async def Yonohate(self):
        if not self.black_out:
            db = Database.getInstance()
            db.close()
            self.hoshizora(f"Close server...")
            self.__state.set_result(True)
            await self._soul.Yonohate()
            self.hoshizora(f"See you next time ^o^")

    async def __aenter__(self):
        return self._soul

    async def __aexit__(self, *args):
        await self.Yonohate()
