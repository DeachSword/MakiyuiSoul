"""
ᖘ    ⋆ • ⋆ • ⋆ ✦ • ⋆ • ⋆      ᖗ
  ♪ ✰ ♪ ꒰ᐢ⸝⸝魔•༝•法⸝⸝ᐢ꒱ ♪ ✰ ♪
ᖚ    ⋆ • ⋆ • ⋆ ✦ • ⋆ • ⋆      ᖙ
"""

import ctypes
import io
from struct import pack, unpack
import sys
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from .warutsu import Warutsu
else:
    Warutsu = sys.modules["LibMasquerade!Warutsu"]


class Mahou:
    @staticmethod
    async def encodeData(
        reqIdx: Optional[int],
        payload: Any = None,
        respType: int = 3,
        rpcName: Optional[str] = None,
    ) -> bytes:
        """Encode data."""
        data = [respType]  # resp type
        if respType != 1:
            data += list(pack("I", reqIdx))
        data += [10]
        if rpcName is None:
            data += [0]  # empty name
        else:
            bRpcName = rpcName.encode()
            data += __class__.writeVarint(len(bRpcName))
            data += list(bRpcName)
        data += [18]
        if payload is None:
            data += [0]  # empty payload
        else:
            data2 = []
            for ii in payload:
                if isinstance(ii, Warutsu):
                    data2 += list(ii)
                else:
                    data2.append(ii)
            data += __class__.writeVarint(len(data2))
            data += data2
        return bytes(data)

    @staticmethod
    async def decodeData(data: bytes, tryDecodrGroupData: bool = False):
        """Decode socket stream data."""
        headerType, reqIdx, data = await __class__.readHeaders(data)
        rpcName, rpcData = await __class__.readRpc(data)
        if rpcData != b"":
            rpcData = __class__.readProto(
                rpcData, tryDecodrGroupData=tryDecodrGroupData
            )
        else:
            rpcData = None
        return rpcName, rpcData, reqIdx

    @staticmethod
    def readProto(
        data: bytes, data_dict: Optional[dict] = None, tryDecodrGroupData: bool = False
    ):
        """Read protobuf."""
        reader = io.BytesIO(data)
        val = __class__.readVarint(reader)
        _type = val & 0b111
        _idx = val >> 3
        _data = None
        if data_dict is None:
            data_dict = {}
        if _type == 0:
            # VARINT
            _data = __class__.readVarint(reader)
        elif _type == 1:
            # I64
            vi64 = __class__.readVarint(reader)
            _data = fromZigZag(vi64)
        elif _type == 2:
            # LEN
            ls = int(__class__.readVarint(reader))
            _data = reader.read(ls)
            try:
                # maybe utf8 string
                _str = _data.decode()
                if len(_str) == len(_data):
                    _data = _str
            except:
                # maybe field?
                if tryDecodrGroupData:
                    _data = __class__.readProto(_data)
        elif _type == 3:
            # SGROUP
            # deprecated
            raise RuntimeError(f"Got SGROUP")
        elif _type == 4:
            # EGROUP
            # deprecated
            raise RuntimeError(f"Got EGROUP")
        else:
            raise NotImplementedError(f"未知 proto type: {_type}, field: {_idx}")
        if _idx in data_dict:
            # repeated
            if isinstance(data_dict[_idx], list):
                data_dict[_idx].append(_data)
            else:
                old_data = data_dict[_idx]
                data_dict[_idx] = [old_data, _data]
        else:
            data_dict[_idx] = _data
        left_data = reader.read()
        if left_data:
            return __class__.readProto(left_data, data_dict)
        return data_dict

    @staticmethod
    def writeVarint(data: int, bits: int = 0):
        """Write varint."""
        if not isinstance(data, int):
            raise ValueError(f"writeVarint expects int, but got {data}")
        out = []
        data = ctypes.c_uint32(data).value
        if bits > 0:
            data = makeZigZag(data, bits)
        while True:
            if data & ~0x7F == 0:
                out.append(data)
                break
            else:
                out.append((data & 0xFF) | 0x80)
                data = data >> 7
        return out

    @staticmethod
    def readVarint(reader):
        """Read varint."""
        result = 0
        shift = 0
        i = 0
        while True:
            byte = list(reader.read(1))[0]
            i += 1
            result |= (byte & 0x7F) << shift
            if byte >> 7 == 0:
                return result
            shift += 7

    @staticmethod
    async def readHeaders(data):
        """Read header data."""
        # read type
        #   0 "NULL"
        #   1 "NOTIFY"
        #   2 "REQUEST"
        #   3 "RESPONSE"
        _type = data[0]

        # read reqIndex
        (reqIndex,) = unpack("h", data[1:3])
        return _type, reqIndex, data[3:]

    @staticmethod
    async def readRpc(data):
        """Read rpc data."""
        reader = io.BytesIO(data)
        _t = list(reader.read(1))[0]
        if _t == 10:
            # read name
            _ls = __class__.readVarint(reader)
            _n = reader.read(_ls)
        else:
            raise RuntimeError(f"未知rpc call type: {_t}")
        _t = list(reader.read(1))[0]
        if _t == 18:
            # read data
            _ls = __class__.readVarint(reader)
            _d = reader.read(_ls)
        else:
            raise RuntimeError(f"未知rpc call type: {_t}")
        return _n.decode(), _d

    @staticmethod
    def EnDecode(data: bytes) -> bytes:
        data = bytearray(data)
        B = [132, 94, 78, 66, 57, 162, 31, 96, 28]
        for i in range(len(data)):
            G = (23 ^ len(data)) + 5 * i + B[i % len(B)] & 255
            data[i] ^= G
        return bytes(data)

    @staticmethod
    def convertFieldValByType(field_type: str, val) -> Any:
        if field_type in ["uint32", "int32"]:
            val = int(val)
        elif field_type == "bool":
            val = bool(val)
        else:
            raise ValueError("unknown type: {field_type}")
        return val

    @staticmethod
    def getFieldTypeForWarutsu(field_type: str) -> int:
        if field_type in ["uint32", "int32", "bool"]:
            return 0
        raise ValueError("Can't get field type with unknown type name: {field_type}")


def fromZigZag(n: int) -> int:
    return (n >> 1) ^ -(n & 1)


def makeZigZag(n: int, bits: int) -> int:
    return (n << 1) ^ (n >> (bits - 1))
