import os
import shutil

from static_to_public import transfer
from generating_function import generate_page

def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")
    transfer("")

    generate_page("content/index.md", "template.html", "public/index.html")

main()