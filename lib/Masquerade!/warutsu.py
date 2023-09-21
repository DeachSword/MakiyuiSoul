"""
    LaLaLa...

              LaLa
            LaLa
"""

import sys


class Warutsu:
    def __init__(self, field, ttype, data, enDecode: bool = False, zzBits: int = 0):
        self._field = field
        self._ttype = ttype
        self._data = data
        self._enDecode = enDecode
        self._zzBits = zzBits

        self.__mahou = sys.modules["LibMasquerade!Mahou"]

    @property
    def header(self):
        val = self._field << 3 | self._ttype
        vals = self.__mahou.writeVarint(val)
        return vals

    @property
    def body(self):
        d = []
        if self._ttype == 0:
            if self._data == '':
                raise ValueError(f"Got empty string: {self}")
            d += self.__mahou.writeVarint(self._data, self._zzBits)
        elif self._ttype == 2:
            if isinstance(self._data, list):
                d2 = []
                for d3 in self._data:
                    d2 += list(d3)
            elif isinstance(self._data, str):
                d2 = []
                for d3 in self._data.encode():
                    d2.append(d3)
            else:
                d2 = list(self._data)
            if self._enDecode:
                d2 = self.__mahou.EnDecode(d2)
            d += self.__mahou.writeVarint(len(d2))
            d += d2
        else:
            raise ValueError(f"Not support ttype: {self._ttype}")
        return d

    def __iter__(self):
        for i in self.header + self.body:
            yield i

    def __len__(self):
        return len(self.header + self.body)

    def __repr__(self):
        L = ["%s=%r" % (key, value) for key, value in self.__dict__.items()]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(L))
