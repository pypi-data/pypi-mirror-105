import json
import os, sys
from pathlib import Path


def main():
    jsonpath = sys.argv[1]

    assert ".json" in jsonpath

    filename = Path(jsonpath)
    dirname = filename.with_suffix('')

    os.mkdir(dirname)

    with open(filename) as f:
        contents = json.loads(f.read())

    for c, c_idx in zip(contents, range(len(contents))):
        each_path = "{0}/{1}.json".format(dirname, c_idx)
        with open(each_path, "w") as f:
            json.dumps(c, f, indent=4)
