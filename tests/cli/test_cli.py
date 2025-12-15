import json
import os
import shutil
import subprocess
import time
from pathlib import Path


def test_cli(tmp_path):
    newdir = tmp_path / "cli"
    newdir.mkdir()
    os.chdir(Path(__file__).parent)
    shutil.copytree(".", newdir, dirs_exist_ok=True)
    os.chdir(newdir)
    subprocess.run(["pyslice"], input="\ny\n", text=True, check=True)
    time.sleep(60)
    dirs = sorted([str(i.as_posix()) for i in sorted(list(Path("output").rglob("*")))])
    dirs = [i for i in dirs if "pyslice.log" not in i]
    refdirs = sorted(json.load(open("refdirs.json")))
    refdirs = [i for i in refdirs if "pyslice.log" not in i]
    assert dirs == refdirs
