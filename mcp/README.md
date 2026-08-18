# TRU8 public MCP server

**Less is more. We dropped the E.**

Public demo MCP for [TRU8](https://github.com/ceedot-rock/TRU8) by Slid Phi Labs.  
Exposes **only** public specialty tokens. No private residual engine.

## Tools

| Tool | Token | What it does |
|------|--------|----------------|
| `demo_zeros` | T_ZERO | Pack a long run → fixed **8 B** |
| `demo_trisum` | T_TRISUM_HOT | Hot trigram → 2 B def + 1 B ids (~66% on matched) |
| `demo_dict` | T_DICT | Exact block hits → **8 B** ptr each (128× on 1 KB) |
| `token_map` | — | Public token map (licensed paths listed, not exposed) |

## Resources / prompts

- Resource `tru8://readme` — short product blurb  
- Prompt `specialty_proof` — safe public messaging template  

## Run

```bash
pip install "mcp[cli]"
uv run mcp dev mcp/server.py
# or self-test:
python3 mcp/server.py
```

## Cursor / Claude config example

```json
{
  "mcpServers": {
    "tru8": {
      "command": "python3",
      "args": ["/path/to/TRU8/mcp/server.py"]
    }
  }
}
```

## IP

- Public demos only (`T_ZERO`, `T_DICT`, `T_TRISUM_HOT`)
- **Not** exposed: T_SPARSE, full residual coefficients, Continuous-1088 Strong
- Credit required: **Powered by TRU8 · Slid Phi Labs**
- Commercial license: license@slidphilabs.com

## Spec

Built against the official MCP Python SDK (tools / resources / prompts).  
See https://modelcontextprotocol.io/docs/sdk
