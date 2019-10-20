picsort
=====================================================
This script is mainly used to handle the images copied from an iPhone. Images on an iPhone are all stored in the same directory, no matter whether they were actually taken with the iPhone or received via some messenger. Additionally, videos are stored in the exact same directory.

The first task I intended to solve with this script was to filter out the videos. I'm just interested in copying the images. The second task was to split the images taken with the iPhone and all the others in two different directories. Finally, the images that have been taken with the iPhone get sorted based on their recording date and the recording date is added as prefix to the filename of each image. The recording date is part of the meta data ([EXIF](https://de.wikipedia.org/wiki/Exchangeable_Image_File_Format)) of each image that was captured by the iPhone. This information is suitable to differentiate between received images and own images, because messengers typically delete an image's meta data before transferring it.

So, in general the script copies all images (and only images) from the input directory and splits them into two sets. The first one contains the sorted images with meta data and the second one contains the unsorted images without meta data.

### DEPENDENCIES
- **[Pillow](https://pillow.readthedocs.io/en/stable/)** --> pip3 install pillow

### USAGE
```
$ ./picsort.py -d <input_directory>
```
