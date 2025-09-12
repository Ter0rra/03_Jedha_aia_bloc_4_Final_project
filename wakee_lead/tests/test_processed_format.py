import os

def check_format(src="./data/processed"):
    for file in os.listdir(src):
        if not file.lower().endswith((".jpg", ".jpeg")):
            raise ValueError(f"Unexpected file format found in {src} !")
        
def test_check_format():
    src="./data/processed"
    check_format(src)
    assert all(file.endswith(".jpg") for file in os.listdir(src))