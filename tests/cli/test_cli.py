import json
import os
import shutil
import subprocess
from pathlib import Path


def test_cli(tmp_path):
    newdir = tmp_path / "cli"
    newdir.mkdir()
    os.chdir(Path(__file__).parent)
    shutil.copytree(".", newdir, dirs_exist_ok=True)
    os.chdir(newdir)
    subprocess.run(["pyslice"], input="\ny\n", text=True, check=True)
    dirs = [str(i) for i in sorted(list(Path("output").rglob("*")))]
    refdirs = json.load(open("refdirs.json"))
    assert dirs == refdirs
