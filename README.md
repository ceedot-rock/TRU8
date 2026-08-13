# TRU8

**Less is more. We dropped the E.**

TRU8 turns repetition into true minimal units.

```
T_ZERO       0x00   dormant run        → 8 B
T_DICT       0x01   1 KB exact hit     → 8 B ptr   (128×)
T_TRISUM_HOT 0x10   hot trigram        → 1 B id    (66% on matched)
```

Public demo surface by **Slid Phi Labs**.  
Production residual engine is commercially licensed.

## Quick demos

```bash
python -m tru8
```

| Demo | Raw | TRU8 | Result |
|------|-----|------|--------|
| 1 000 000 zeros | 1 MB | 8 B | **125 000×** |
| `"the"` × 1000 | 3000 B | 1002 B | **66.6% saving** |
| 100 × 1 KB dups | 102400 B | 800 B | **128×** |

## Install (demo)

```bash
pip install -e .
python -m tru8
```

## Token map

```python
T_ZERO       = 0x00
T_DICT       = 0x01
T_SPARSE     = 0x03   # 128² residual (licensed path)
T_TRISUM_HOT = 0x10
```

TriSum packing (public):

```python
def tri_to_sum(c0, c1, c2):
    return (c0 << 10) | (c1 << 5) | c2   # 15 bits → 2 B definition
```

## License

Public demo only. See [LICENSE](LICENSE).  
Credit required: **Powered by TRU8 · Slid Phi Labs**  
Full engine / residual: commercial license — license@slidphilabs.com

## Brand

TRU8 · Less is more.
