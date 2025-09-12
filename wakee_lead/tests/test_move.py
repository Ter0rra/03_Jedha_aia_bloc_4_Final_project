import os
import shutil

def bash_mv(src="./src/temp", dst="./data/raw_images"):
    for file in os.listdir(src):
        if file.lower().endswith((".jpg", ".png", ".jpeg")):
            shutil.move(os.path.join(src, file), os.path.join(dst, file))

def test_bash_mv():
    src="./src/temp"
    dst="./data/raw_images"
    bash_mv(src, dst)
    assert any(file.endswith(".jpg") for file in os.listdir(dst))
