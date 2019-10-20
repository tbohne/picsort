#!/usr/bin/env python3

"""
PICSORT

Script to filter images and sort them based on recording date.
"""

from PIL import Image, ExifTags
from datetime import datetime
from argparse import ArgumentParser
import shutil
import os
import re

def copy_meta_data_img(date, image, filename, extension):
    """
    Copies image containing meta data.
    :param date:      recording date of the image
    :param image:     image to be copied
    :param filename:  filename of the image
    :param extension: extension of the image
    """
    if not os.path.exists(output_dir_sorted):
        os.makedirs(output_dir_sorted)
    shutil.copy2(os.path.join(input_dir, image), output_dir_sorted
                 + "/" + date + "_" + filename + "." + extension.lower())

def copy_no_data_img(image, filename, extension):
    """
    Copies image without meta data.
    :param image:     image to be copied
    :param filename:  filename of the image
    :param extension: extension of the image
    """
    if not os.path.exists(output_dir_unsorted):
        os.makedirs(output_dir_unsorted)
    shutil.copy2(os.path.join(input_dir, image), output_dir_unsorted
                 + "/" + filename + "." + extension.lower())

def parse_date(img_exif):
    """
    Parses the recording date from an image's EXIF data.
    :param img_exif: EXIF data to be parsed
    :return parsed recording date / none
    """
    img_exif_dict = dict(img_exif)
    for key, val in img_exif_dict.items():
        if key in ExifTags.TAGS:
            entry = f"{ExifTags.TAGS[key]}:{repr(val)}"
            if "DateTimeOriginal" in entry:
                return entry.split("'")[1].strip()
    return None

def picsort():
    """
    Performs the actual filtering / copying / sorting procedure.
    """
    for image in os.listdir(input_dir):
        filename_matches = re.finditer(img_regex, image, re.UNICODE)
        filename, extension = None, None
        for match in filename_matches:
            filename, extension = match.groups()
        if not filename or not extension:
            continue

        img = Image.open(os.path.join(input_dir, image))
        img_exif = img.getexif()

        if img_exif:
            date = parse_date(img_exif)
            image_time = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
            day_str = image_time.strftime("%Y_%m_%d_%A")
            copy_meta_data_img(day_str, image, filename, extension)
        else:
            print("The file " + os.path.join(input_dir, image) + " has no exif data.")
            copy_no_data_img(image, filename, extension)

if __name__ == '__main__':
    parser = ArgumentParser(description = "Filter images and sort them based on recording date.")
    parser.add_argument("-d", "--directory", type = str, required = True, metavar = "", help = "directory of input images")
    args = parser.parse_args()
    input_dir = args.directory

    if os.path.exists(input_dir):
        dirname = os.getcwd()
        output_dir_unsorted = dirname + "/output/unsorted"
        output_dir_sorted = dirname + "/output/sorted"
        img_regex = r"(?P<filename>.*)\.(?P<extension>JPG|jpg|jpeg|PNG|png|tiff|tif|TIF|BMP|bmp)"
        picsort()
    else:
        print("Invalid input directory.")

