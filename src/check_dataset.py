import os

data_path = 'dataset/'

if not os.path.exists(data_path):
    print(f"[ERROR] Dataset path not found: {data_path}")
else:
    print(f"[INFO] Dataset path exists: {data_path}")
    files = os.listdir(data_path)
    if not files:
        print("[ERROR] Dataset folder is empty!")
    else:
        print(f"[INFO] Files in dataset folder: {files}")
