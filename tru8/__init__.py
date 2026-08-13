"""TRU8 — true minimal units for repetition. Public demo surface."""
__version__ = "0.1.0"
from .core import (
    T_ZERO, T_DICT, T_SPARSE, T_TRISUM_HOT,
    tri_to_sum, sum_to_tri,
    pack_zero_run, pack_dict_ptr, pack_trisum_hot,
    demo_zeros, demo_trigram, demo_dict_block,
)
