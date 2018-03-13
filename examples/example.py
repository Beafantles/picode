from picode import picode
from os import listdir
from os.path import isfile, join
import os

dir = os.path.dirname(__file__)
codes_dir = os.path.join(dir, "codes")
images_dir = os.path.join(dir, "images")

if not os.path.exists(images_dir):
    os.makedirs(images_dir)

code_files = [f for f in listdir(codes_dir) if isfile(join(codes_dir, f))]

for code_file in code_files:
    im = picode.to_pic(file_path=codes_dir + "/" + code_file)
    im.save(images_dir + "\\" + code_file.replace(".", "_") + ".png")
