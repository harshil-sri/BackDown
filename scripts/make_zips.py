"""Build dist/BackDown-for-<Name>.zip from the committed HEAD plus a START_HERE.md brief.

python scripts/make_zips.py
"""

import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PEOPLE = [("Daksh", "docs/team/DAKSH.md"), ("Kartik", "docs/team/KARTIK.md")]


def main():
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    for who, brief in PEOPLE:
        z = dist / f"BackDown-for-{who}.zip"
        z.unlink(missing_ok=True)
        subprocess.run(["git", "archive", "--format=zip", "--prefix=BackDown/", "-o", str(z), "HEAD"], cwd=ROOT, check=True)
        note = (f"# START HERE ({who})\n\nSnapshot of commit {head}. Give this folder to your agent and tell it: "
                f"read {brief} first, then docs/SPEC.md and docs/CONTRACT.md.\n\n"
                "The live repo is https://github.com/harshil-sri/BackDown. Clone it and `git pull` often; "
                "the repo is newer than this zip.\n\n")
        with zipfile.ZipFile(z, "a", zipfile.ZIP_DEFLATED) as f:
            f.writestr("BackDown/START_HERE.md", note + (ROOT / brief).read_text(encoding="utf-8"))
        print(f"{z.relative_to(ROOT)} ({z.stat().st_size // 1024} KB, commit {head})")


if __name__ == "__main__":
    main()
