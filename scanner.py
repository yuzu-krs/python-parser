import os
import sys

if len(sys.argv) != 2:
    print("使用法: python script.py <ファイル名>")
    sys.exit(1)

file_path = sys.argv[1]

with open(file_path, "r", encoding="utf-8") as file:
    for char in file.read():
        print(char)
