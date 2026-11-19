"""Load and query the entity failure catalog."""
from pathlib import Path


CATALOG_DIR = Path(__file__).resolve().parent.parent.parent / "catalog"


def load_catalog():
    """Load all catalog JSON files and return a dict keyed by entity type."""
    import json
    catalog = {}
    for f in sorted(CATALOG_DIR.glob("*.json")):
        data = json.loads(f.read_text())
        catalog[data["type"]] = data
    return catalog
