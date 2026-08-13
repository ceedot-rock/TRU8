# TRU8 Chamber Smart Shell

Public path. Lend-to-codebases black-box shape.

```
raw → compress → φ-split → lock → k_words + r_words
unlock: both streams + nonce + tag + password → raw
```

## Run demo

```bash
python -m chamber.shell
```

## Shape

- `ChamberShell.pack(raw)` → chamber dict
- `ChamberShell.unpack(chamber)` → raw
- HMAC verified before open
- Word streams are derived labels, not the key

## License

Public demo shell only.  
Production residual / full `_call_core` remains commercially licensed.  
Credit: **Powered by TRU8 · Slid Phi Labs**

[Request commercial license](mailto:license@slidphilabs.com?subject=TRU8%20Commercial%20License%20Inquiry)
