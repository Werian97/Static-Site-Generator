import os
import shutil

from static_to_public import transfer
from generating_function import generate_pages_recursive

def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")
    transfer("")

    generate_pages_recursive("content", "template.html", "public")

main()