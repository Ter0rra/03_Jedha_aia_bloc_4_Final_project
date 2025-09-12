import os

def check_format(src="./data/processed"):
    for file in os.listdir(src):
        if file.lower().endswith((".jpg", ".jpeg")):
            return True
        
def test_check_format():
    src="./data/processed"
    assert all(file.endswith(".jpg") for file in os.listdir(src))