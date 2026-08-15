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

## Specialty proof

| Demo | Raw | TRU8 | Result |
|------|-----|------|--------|
| 1 000 000 zeros | 1 MB | 8 B | **125 000×** |
| `"the"` × 1000 | 3000 B | 1002 B | **66.6% saving** |
| 100 × 1 KB dups | 102400 B | 800 B | **128×** |

```bash
npm i @cptasz13/tru8
npx @cptasz13/tru8
```

Python:

```bash
pip install -e .
python -m tru8
```

## Competitive proof

General compressors are strong on the whole file.  
TRU8 is stronger on the structure inside it — and the full stack hangs with them on the rest.

| Set | zstd-19 | TRU8 public stack | Note |
|-----|---------|-------------------|------|
| Text-heavy Silesia (~119 MB) | ~15.9% | residual path closes the gap | hangs |
| Matched structure (tris / 1 KB / runs) | full LZ cost | **66–128×+** on claimed units | wins |
| Long zero / ramp runs | good | **8 B** fixed | owns |

> We claim structure harder. We hang on the residual.

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

## Install (demo)

```bash
pip install -e .
python -m tru8
```

## License

Public demo only. See [LICENSE](LICENSE).  
Credit required: **Powered by TRU8 · Slid Phi Labs**

### Commercial license inquiry

Full residual engine, production packer, and Continuous-1088 Strong path are available under commercial license.

**[Request a commercial license →](mailto:corey@slidphilabs.com?subject=TRU8%20Commercial%20License%20Inquiry)**

Or email: [corey@slidphilabs.com](mailto:corey@slidphilabs.com)

## Brand

TRU8 · Less is more.
