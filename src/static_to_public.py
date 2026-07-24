import os
import shutil

STATIC = "./static"
PUBLIC = "./public"

def transfer(filepath: str):
    src_dir: str = os.path.join(STATIC, filepath)
    dst: str = os.path.join(PUBLIC, filepath)
    if not os.path.exists(dst):
        os.mkdir(dst)
    files: list[str] = os.listdir(src_dir)
    for file in files:
        src = os.path.join(src_dir, file)
        if os.path.isdir(src):
            transfer(os.path.join(filepath, file))
        else:
            shutil.copy(src, dst)