import os
import shutil
import sys

from static_to_public import transfer
from generating_function import generate_pages_recursive

def main():
    basepath: str = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")
    transfer("")

    generate_pages_recursive("content", "template.html", "docs", basepath)

main()