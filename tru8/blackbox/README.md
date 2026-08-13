# TRU8 product blackboxes

One blackbox per product surface. Callers only see `pack` / `unpack`.

| Box | Token | Public |
|-----|-------|--------|
| `ZeroBox` | T_ZERO | yes — 8 B runs |
| `DictBox` | T_DICT | yes — 8 B / 1 KB |
| `TrisumBox` | T_TRISUM_HOT | yes — 1 B ids |
| `ChamberShell` | chamber/ | yes — φ-split lock |
| `ResidualBox` | residual | **stub only — licensed** |

## Container: `.tru8` (not `.Tru3`)

```
magic 4B  "TRU8"
mode  1B  0=zero 1=dict 2=trisum 3=chamber 0xFF=residual
flags 1B
plen  4B
payload
```

Optional chamber-wrapped files: `.tru8c`

## License

Public boxes free with credit: **Powered by TRU8 · Slid Phi Labs**  
Residual / full engine: [commercial license](mailto:license@slidphilabs.com?subject=TRU8%20Commercial%20License%20Inquiry)
