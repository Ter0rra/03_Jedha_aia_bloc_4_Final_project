import os

def check_format(src="./data/raw_images"):
    for file in os.listdir(src):
        if not file.lower().endswith((".jpg", ".jpeg")):
            raise ValueError()
        
def test_check_format():
    src="./src/temp"
    check_format(src)
    assert all(file.endswith(".jpg") for file in os.listdir(src))