# src/report/report_generator.py
import json

def generate_json_report(results, path="report.json"):
    with open(path, "w") as f:
        json.dump(results, f, indent=4)
