from .core import demo_zeros, demo_trigram, demo_dict_block

def main():
    print("TRU8 public demos — Slid Phi Labs")
    print("Less is more. We dropped the E.\n")
    for d in (demo_zeros(), demo_trigram(), demo_dict_block()):
        print(f"[{d['token']}] {d['name']}")
        print(f"  raw:  {d['raw_bytes']:,} B")
        print(f"  TRU8: {d['tru8_bytes']:,} B")
        if "ratio" in d:
            print(f"  ratio: {d['ratio']:,.0f}×")
        if "ratio_saving_pct" in d:
            print(f"  saving: {d['ratio_saving_pct']:.1f}%")
        if "sum_hex" in d:
            print(f"  sum: {d['sum_hex']}")
        print()

if __name__ == "__main__":
    main()
