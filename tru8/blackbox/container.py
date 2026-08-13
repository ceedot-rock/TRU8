"""
TRU8 product archive family

  TrUw  (.truw)  — wrap / general archive
  TrUc  (.truc)  — chamber-locked shell
  TrUnK (.trunk) — multi-mode trunk container

Header (all three share the same layout):
  magic  4B   b"TRUW" | b"TRUC" | b"TRNK"
  mode   1B   0=zero 1=dict 2=trisum 3=chamber 0xFF=residual(licensed)
  flags  1B   reserved
  plen   4B   payload length (little-endian)
  payload ...
"""
from __future__ import annotations
import struct

MAGIC_TRUW = b"TRUW"
MAGIC_TRUC = b"TRUC"
MAGIC_TRUNK = b"TRNK"

MODE_ZERO = 0x00
MODE_DICT = 0x01
MODE_TRISUM = 0x02
MODE_CHAMBER = 0x03
MODE_RESIDUAL = 0xFF

EXT_TRUW = ".truw"
EXT_TRUC = ".truc"
EXT_TRUNK = ".trunk"

def write_truw(mode: int, payload: bytes, flags: int = 0) -> bytes:
    return MAGIC_TRUW + struct.pack("<B B I", mode & 0xFF, flags & 0xFF, len(payload)) + payload

def write_truc(payload: bytes, flags: int = 0) -> bytes:
    return MAGIC_TRUC + struct.pack("<B B I", MODE_CHAMBER, flags & 0xFF, len(payload)) + payload

def write_trunk(mode: int, payload: bytes, flags: int = 0) -> bytes:
    return MAGIC_TRUNK + struct.pack("<B B I", mode & 0xFF, flags & 0xFF, len(payload)) + payload

def read_archive(blob: bytes) -> tuple[str, int, int, bytes]:
    if len(blob) < 10:
        raise ValueError("truncated archive")
    magic = blob[:4]
    mode, flags, plen = struct.unpack_from("<B B I", blob, 4)
    payload = blob[10 : 10 + plen]
    if len(payload) != plen:
        raise ValueError("truncated payload")
    if magic == MAGIC_TRUW:
        kind = "truw"
    elif magic == MAGIC_TRUC:
        kind = "truc"
    elif magic == MAGIC_TRUNK:
        kind = "trunk"
    else:
        raise ValueError(f"unknown magic {magic!r} — expected TRUW/TRUC/TRNK")
    return kind, mode, flags, payload

write_tru8 = write_truw
EXTENSION = EXT_TRUW
CHAMBER_EXTENSION = EXT_TRUC
