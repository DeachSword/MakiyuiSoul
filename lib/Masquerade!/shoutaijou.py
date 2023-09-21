"""  / / / / / / / / / / / / / / /
    /                    招待状　/
   /                           /
  /                 - 午前0時　/
 / / / / / / / / / / / / / / /
"""

from functools import wraps
import sys
from websockets import WebSocketServerProtocol

魔法 = sys.modules["LibMasquerade!Mahou"]
わるつ = sys.modules["LibMasquerade!Warutsu"]


class 深紅の紅玉:
    """Client req"""

    def __init__(self) -> None:
        pass


class 暗闇の舞台(WebSocketServerProtocol, 魔法):
    """Server resp"""

    def __init__(ctx: WebSocketServerProtocol) -> WebSocketServerProtocol:
        for ss in dir(__class__):
            if ss.startswith("Resp"):
                fn = getattr(__class__, ss)
                時を忘れ(ctx, fn)
        return ctx

    async def RespCommon(self, reqIdx: int, data: any = None) -> None:
        await self.send(await __class__.encodeData(reqIdx, data))

    async def RespNotify(self, name: str, data: any = None):
        await self.send(await __class__.encodeData(None, data, 1, name))

    async def RespErr(self, reqIdx: int, errCode: int, field: int = 0) -> None:
        err = わるつ(1, 0, errCode)
        await self.send(await __class__.encodeData(reqIdx, わるつ(field, 2, err)))

    async def RespLobbyHeatbeat(self, reqIdx: int) -> None:
        await self.send(await __class__.encodeData(reqIdx))

    async def RespActionPrototype(self, step: int, name: str, data: any) -> None:
        ActionPrototype = [
            わるつ(1, 0, step),
            わるつ(2, 2, name),  # name
            わるつ(3, 2, data, True),  # data
        ]
        await self.RespNotify(".lq.ActionPrototype", ActionPrototype)


def 時を忘れ(ctx: any, fn: any):
    @wraps(fn)
    async def __fn(*args):
        await fn(ctx, *args)

    setattr(ctx, fn.__name__, __fn)
