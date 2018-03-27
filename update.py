import requests, zipfile
import shutil
from shutil import copyfile
from clint.textui import progress
import os
import time, sys
import psutil


def update():
    try:
        if not os.path.exists("update"):
            os.makedirs("update")
        path = 'update/master.zip'
        url = "https://github.com/Bamux/RiftEventTracker/archive/master.zip"

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
        for file in zf.infolist():
            extracted_size += file.file_size
            i = int((extracted_size * 100 / uncompress_size))
            print('\rExtract files: %3d%%' % i, end='', flush=True)
            time.sleep(0.1)
            zf.extract(file, "update")
        zf.close()

        copyfile('update/RiftEventTracker-master/update.exe', '_update.exe')
        copyfile('update/RiftEventTracker-master/README.md', 'README.md')
        copyfile('update/RiftEventTracker-master/RiftEventTracker.exe', 'RiftEventTracker.exe')

        files = os.listdir("update/RiftEventTracker-master")
        for f in files:
            if f != ".gitignore":
                if not os.path.exists(f):
                    shutil.move("update/RiftEventTracker-master/" + f, ".")

        shutil.rmtree("update")
        print("\nProgram successfully updated!")
        os.system("RiftEventTracker.exe")
    except:
        time.sleep(1)
        update()

PROCNAME = "RiftEventTracker.exe"
for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == PROCNAME:
        proc.kill()

print("A new version of RiftEvenetTracker is available. Update started:")
update()
