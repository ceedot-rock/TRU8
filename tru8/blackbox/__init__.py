"""TRU8 product blackboxes — one box per product surface."""
from .zero import ZeroBox
from .dict_box import DictBox
from .trisum import TrisumBox
from .residual import ResidualBox, NotLicensed
from .container import (
    write_truw, write_truc, write_trunk, read_archive,
    EXT_TRUW, EXT_TRUC, EXT_TRUNK,
    MODE_ZERO, MODE_DICT, MODE_TRISUM, MODE_CHAMBER,
    MAGIC_TRUW, MAGIC_TRUC, MAGIC_TRUNK,
)

__all__ = [
    "ZeroBox", "DictBox", "TrisumBox", "ResidualBox", "NotLicensed",
    "write_truw", "write_truc", "write_trunk", "read_archive",
    "EXT_TRUW", "EXT_TRUC", "EXT_TRUNK",
    "MODE_ZERO", "MODE_DICT", "MODE_TRISUM", "MODE_CHAMBER",
]
