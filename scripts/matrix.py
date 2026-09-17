"""Turn bundles.json into a GitHub Actions build matrix.

Usage: matrix.py "<comma-separated bundle names, or blank for all>"
Prints `matrix=<json>` for $GITHUB_OUTPUT.
"""
import json
import sys

DRIVERS = "src/mame/drivers/"

bundles = json.load(open("bundles.json"))
wanted = [b.strip() for b in (sys.argv[1] if len(sys.argv) > 1 else "").split(",") if b.strip()]
unknown = [b for b in wanted if b not in bundles]
if unknown:
    sys.exit(f"unknown bundles: {', '.join(unknown)}")

include = [
    {"name": name, "sources": ",".join(s if "/" in s else DRIVERS + s for s in sources)}
    for name, sources in bundles.items()
    if not wanted or name in wanted
]
print("matrix=" + json.dumps({"include": include}))
