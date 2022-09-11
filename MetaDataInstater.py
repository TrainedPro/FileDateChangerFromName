from exif import Image
import os
import shutil
from datetime import datetime
from win32_setctime import setctime
import re
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

inputfilepath = filedialog.askdirectory()

outputfilepath = filedialog.askdirectory()

InputPath = inputfilepath

OutputPath = outputfilepath

try:
    original_umask = os.umask(0)
    os.makedirs(f'{OutputPath}\\Completed', 0o755, exist_ok=True)
finally:
    os.umask(original_umask)

try:
    original_umask = os.umask(0)
    os.makedirs(f'{OutputPath}\\Failed', 0o755, exist_ok=True)
finally:
    os.umask(original_umask)


def ChangeData(file, ExpName):
    with open(InputPath + '/' + file, 'rb') as InputImg:
        img = Image(InputImg)
        print(f'Old MetaData{img.get_all()}')

        # Date Extraction
        ImageName = ExpName.removesuffix('.jpg')

        year, month, day = int(ImageName[0:4]), int(ImageName[4:6]), int(ImageName[6:8])

        hour, minute, second = int(ImageName[9:11]), int(ImageName[11:13]), int(ImageName[13:15])

        # Start To Modify The Required Values
        new_date = datetime(year, month, day, hour, minute, second).strftime("%Y:%m:%d %H:%M:%S")
        epochtime = int(datetime(year, month, day, hour, minute, second).timestamp())

        img.datetime_original, img.datetime_digitized, img.datetime = new_date, new_date, new_date
    with open(f'{OutputPath}\\Completed\\{ExpName}.jpg', 'wb') as OutputImg:
        OutputImg.write(img.get_file())
        print(f'New MetaData{img.get_all()}')

    os.utime(f'{OutputPath}\\Completed\\{ExpName}.jpg', (epochtime, epochtime))
    setctime(f'{OutputPath}\\Completed\\{ExpName}.jpg', epochtime)


    # Process Complete

print('All Files are:',os.listdir(InputPath))

UndoneFiles = []

for file in os.listdir(InputPath):

    ExpNameWithout = re.search("[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9][0-9][0-9]", file)

    if ExpNameWithout:
        ExpName = ExpNameWithout.group()
        ChangeData(file, ExpName)
    else:
        UndoneFiles.append(file)
        shutil.copy(f'{InputPath}\\{file}', f'{OutputPath}\\Failed\\{file}')

print(f'Number Of Failed Files: {len(UndoneFiles)}')

print(f'Failed Files Are: {UndoneFiles}')