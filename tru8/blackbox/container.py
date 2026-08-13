"""
.tru8 container — public product archive format.

Header:
  magic  4B  b"TRU8"
  mode   1B  0=zero 1=dict 2=trisum 3=chamber 0xFF=residual(licensed)
  flags  1B  reserved
  plen   4B  payload length (little-endian)
  payload ...
"""
from __future__ import annotations
import struct

MAGIC = b"TRU8"
MODE_ZERO = 0x00
MODE_DICT = 0x01
MODE_TRISUM = 0x02
MODE_CHAMBER = 0x03
MODE_RESIDUAL = 0xFF

def write_tru8(mode: int, payload: bytes, flags: int = 0) -> bytes:
    return MAGIC + struct.pack("<B B I", mode & 0xFF, flags & 0xFF, len(payload)) + payload

def read_tru8(blob: bytes) -> tuple[int, int, bytes]:
    if len(blob) < 10 or blob[:4] != MAGIC:
        raise ValueError("not a .tru8 archive")
    mode, flags, plen = struct.unpack_from("<B B I", blob, 4)
    payload = blob[10 : 10 + plen]
    if len(payload) != plen:
        raise ValueError("truncated .tru8 payload")
    return mode, flags, payload

EXTENSION = ".tru8"
CHAMBER_EXTENSION = ".tru8c"
