"""Licensed residual blackbox — public stub only."""
MAGIC = b"TRU8R"

class NotLicensed(Exception):
    pass

class ResidualBox:
    MAGIC = MAGIC

    def pack(self, raw: bytes, **kw) -> bytes:
        raise NotLicensed(
            "Production residual is commercially licensed. "
            "Request: license@slidphilabs.com"
        )

    def unpack(self, blob: bytes, **kw) -> bytes:
        raise NotLicensed(
            "Production residual is commercially licensed. "
            "Request: license@slidphilabs.com"
        )
