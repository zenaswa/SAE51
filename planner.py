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

def resolve_dependencies(selection, catalog):
    plan = set(selection)  # A set automatically prevents duplicates
    queue = list(selection) # We process items from this queue

    while queue:
        current = queue.pop(0)

        if current not in catalog:
            print(f"  [Warning] Service '{current}' not found in catalog.")
            continue

        deps = catalog[current].get("depends_on") or []
        for dep in deps:
            if dep not in plan:
                print(f"  [Info] Adding '{dep}' because '{current}' depends on it.")
                plan.add(dep)
                queue.append(dep)
    return plan

def main():
    catalog = load_catalog()
    user_request = []
    print(f"Loaded {len(catalog)} service(s) from {CATALOG_DIR.name}")
    for name, entry in catalog.items():
        describe_service(name, entry)

    print("\nEnter the services you want to deploy, separated by spaces.")
    print("Example: vaultwarden nextcloud")
    user_input = input("> ")
    user_request = user_input.split()
    if not user_request:
        user_request = ["vaultwarden"]

    final_plan = resolve_dependencies(user_request, catalog)

    print("\n--- Final Deployment Plan ---")
    for service in final_plan:
        print(f"  - {service}")
        
if __name__ == "__main__":
    main()
