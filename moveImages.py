import os
import shutil

week_number = "9"
src = f"Grade4_Test_Images/{week_number}"
dest = f"Grade4_Master_Images/{week_number}"

for filename in os.listdir(src):
    src_path = os.path.join(src, filename)
    dest_path = os.path.join(dest, filename)

    shutil.move(src_path, dest_path)