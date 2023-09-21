<h1 align="center">
  MakiyuiSoul<br>
</h1>

<h4 align="center">A server software reimplemented for a Japanese Mahjong game<br><br></h4>

## Join Us

Welcome join our [Discord](https://discord.gg/vQrMbjA)

## Features

- [x] Login / Oauth2
- [x] Characters
- [x] Skins
- [ ] Activitys
- [ ] Multi Game
- [ ] Custom Game
- [ ] Gachas

## Usage/Examples

```python
from . import MakiyuiSoul

MakiyuiSoulServer = MakiyuiSoul()

@MakiyuiSoulServer.Teokure(".lq.Lobby.heatbeat")
async def heatbeat(ctx, payload, reqIdx, *args):
    print('heatbeat!')
    await ctx.RespLobbyHeatbeat(reqIdx)

MakiyuiSoulServer.FutekusaretaNeko()
```

## Config

To run this project, you will need `config.yml` file
