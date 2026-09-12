"""Copy standalone skill guides into Reimagine; --check detects stale copies."""

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check without writing files")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    references = root / "reimagine" / "references"

    # Read both sources before writing anything; this requires a full checkout.
    try:
        sources = {
            name: (root / name / "SKILL.md").read_bytes()
            for name in ("restructure", "compress")
        }
    except OSError as error:
        parser.exit(1, f"Cannot read standalone sources in the full checkout: {error}\n")

    stale = [
        name
        for name, content in sources.items()
        if not (references / f"{name}.md").is_file()
        or (references / f"{name}.md").read_bytes() != content
    ]
    if args.check:
        if stale:
            parser.exit(1, f"Bundled guides missing or stale: {', '.join(stale)}\n")
        print("Bundled guides match standalone sources.")
        return

    for name in stale:
        references.mkdir(parents=True, exist_ok=True)
        (references / f"{name}.md").write_bytes(sources[name])
        print(f"Updated reimagine/references/{name}.md")
    if not stale:
        print("Bundled guides already match standalone sources.")


if __name__ == "__main__":
    main()
