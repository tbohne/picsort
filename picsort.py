#!/usr/bin/env python3

from PIL import Image, ExifTags
from datetime import datetime
import shutil
import os
import re

def copy_meta_data_img(date, image, filename, extension):
    if not os.path.exists(output_folder_sorted):
        os.makedirs(output_folder_sorted)
    shutil.copy2(os.path.join(input_folder, image), output_folder_sorted
        + "/" + date + "_" + filename + "." + extension.lower())

def copy_no_data_img(image, filename, extension):
    if not os.path.exists(output_folder_unsorted):
        os.makedirs(output_folder_unsorted)
    shutil.copy2(os.path.join(input_folder, image), output_folder_unsorted
        + "/" + filename + "." + extension.lower())

def parse_date(img_exif):
    img_exif_dict = dict(img_exif)
    for key, val in img_exif_dict.items():
        if key in ExifTags.TAGS:
            entry = f"{ExifTags.TAGS[key]}:{repr(val)}"
            if "DateTimeOriginal" in entry:
                return entry.split("'")[1].strip()
    return None

def sort_pics():
    for image in os.listdir(input_folder):
        filename_matches = re.finditer(img_regex, image, re.UNICODE)
        filename, extension = None, None
        for match in filename_matches:
            filename, extension = match.groups()
        if not filename or not extension:
            continue

        img = Image.open(os.path.join(input_folder, image))
        img_exif = img.getexif()

        if img_exif:
            date = parse_date(img_exif)
            image_time = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
            day_str = image_time.strftime("%Y_%m_%d_%A")
            copy_meta_data_img(day_str, image, filename, extension)
        else:
            print("The file " + os.path.join(input_folder, image) + " has no exif data.")
            copy_no_data_img(image, filename, extension)

if __name__ == '__main__':
    dirname = os.getcwd()
    input_folder = dirname + "/input"
    output_folder_unsorted = dirname + "/output/unsorted"
    output_folder_sorted = dirname + "/output/sorted"
    img_regex = r"(?P<filename>.*)\.(?P<extension>JPG|jpg|jpeg|PNG|png|tiff|tif|TIF|BMP|bmp)"
    sort_pics()
