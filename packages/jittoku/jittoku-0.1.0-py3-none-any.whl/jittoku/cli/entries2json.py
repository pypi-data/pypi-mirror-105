import json
import os, sys
from pathlib import Path
import glob


def main():
    entries_dir = sys.argv[1]
    filename = Path(entries_dir)
    jsonpath = filename.with_suffix('.json')

    if os.path.exists(jsonpath):
        raise ValueError

    entries = glob.glob(entries_dir + "/*.json")

    results = []

    for e_path in entries:
        with open(e_path) as f:
            each_entry = json.loads(f.read())

        results.append(each_entry)

    with open(jsonpath, "w") as f:
        json.dumps(results, f, indent=4)
