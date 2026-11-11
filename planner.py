#!/usr/bin/env python3

from pathlib import Path
import sys
import yaml

CATALOG_DIR=Path(__file__).parent/"catalog"

def load_catalog():
    if not CATALOG_DIR.is_dir():
        sys.exit(f"Catalog directory not found: {CATALOG_DIR}")
    
    catalog={}
    for file in sorted(CATALOG_DIR.glob("*.yml")):
        with open(file, encoding="utf-8") as f:
            data=yaml.safe_load(f)
            
        if not isinstance(data, dict):
            sys.exit(f"Invalid catalog file (expected a mapping): {file.name}")
        
        for name, entry in data.items():
            if name in catalog:
                sys.exit(f"Duplicate service '{name}'")
            catalog[name] = entry
    
    return catalog
    
def describe_service(name, entry):
    print(f"{name}")
    print(f"    description : {entry['description']}")
    print(f"    image       : {entry['image']}")
    deps = entry.get("depends_on") or []
    if deps:
        print(f"      depends on  : {', '.join(deps)}")



def main():
    catalog = load_catalog()
    print(f"Loaded {len(catalog)} service(s) from {CATALOG_DIR.name}")
    for name, entry in catalog.items():
        describe_service(name, entry)
        
if __name__ == "__main__":
    main()