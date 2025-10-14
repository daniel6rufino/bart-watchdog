# src/analysis/package_parser.py
import json
import os

def parse_package_lock(path: str):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {full_path}")
    
    with open(full_path, "r") as f:
        data = json.load(f)
    dependencies = data.get("dependencies", {})
    return [{"package": package, "version": info.get("version")} for package, info in dependencies.items()]
