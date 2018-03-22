import requests, zipfile
import shutil
from shutil import copyfile
from clint.textui import progress
import os
import time


if not os.path.exists("update"):
    os.makedirs("update")
path = 'update/master.zip'
url = "https://github.com/Bamux/RiftEventTracker/archive/master.zip"
print("Download the latest version:")
r = requests.get(url, stream=True)
with open(path, 'wb') as f:
    total_length = int(r.headers.get('content-length'))
    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
        if chunk:
            f.write(chunk)
            f.flush()

zf = zipfile.ZipFile(path)
uncompress_size = sum((file.file_size for file in zf.infolist()))
extracted_size = 0
percent = 0
old_percent = 0
print("Unpack the file:")
for file in zf.infolist():
    extracted_size += file.file_size
    percent = int((extracted_size * 100 / uncompress_size))
    if percent > old_percent:
        print('{:02}'.format(percent) + " %")
        old_percent = percent
    zf.extract(file, "update")
zf.close()
print("Files will be copied please wait a moment.")
time.sleep(1)

copyfile('update/RiftEventTracker-master/update.exe', '_update.exe')
files = os.listdir("update/RiftEventTracker-master")
for f in files:
    if f != ".gitignore":
        print(f)
        if not os.path.exists(f):
            shutil.move("update/RiftEventTracker-master/" + f, ".")

shutil.rmtree("update")
print("Program successfully updated!")
time.sleep(10)