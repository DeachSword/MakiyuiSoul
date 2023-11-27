class CommonErr(Exception):
    def __init__(self, code: int, fid: int = 1) -> None:
        self.code = code
        self.fid = fid
