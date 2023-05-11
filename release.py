import os
import pathlib
import shutil
import sys


def main():
    dist = pathlib.Path(__file__).parent / "dist"
    shutil.rmtree(dist, ignore_errors=True)
    dist.mkdir()
    shutil.copy(os.environ["TOX_PACKAGE"], dist)


if __name__ == "__main__":
    sys.exit(main())
