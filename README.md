# Blob Cropper

A Python command line tool which uses opencv2 to extract 'blobs' from images or videos. The blob detector used is tuned to target a wide varity of blobs. It attempts to detect circluar blobs, ellipse shaped blobs, or blobs with concavity. The extracted blobs are stored as PNG files in the folder path provided via the application's CMD line interface.

---

## Python Version Required

3.9.6  
_All development done on 3.9.6_

---

## Installation Instructions

1. Clone Repo
2. Using a terminal navigate to root of the project
3. In the terminal execute the command below  
   `pip install -r requirements.txt`

---

## Application Commands

The application has 2 major commands and a help command.

1. Help command  
   `python ./blob_cropper.py --help`

2. Crop images command  
   `python ./blob_cropper.py crop_images -s folder/path/to/my/images -d folder/path/to/empty/folder`

   > The -s flag's value specifies the source folder where images will be retrieved from and processed.  
   > The -d flag's value specifies the destination folder where the extracted blobs will be saved as image files.  
   > &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_If destination folder does not exist one will be created inside the source folder._

3. Crop videos command  
   `python ./blob_cropper.py crop_videos -s folder/path/to/my/videos -d folder/path/to/empty/folder`

   > The -s flag's value specifies the source folder where videos will be retrieved from and processed.  
   > The -d flag's value specifies the destination folder where the extracted blobs will be saved as image files.  
   > &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_If destination folder does not exist one will be created inside the source folder._

---

## Limitations

### Images

The images processed by the module must have extensions supported by opencv2.  
A listing of supported opencv2 image extensions can be found in the [opencv2 docs](https://docs.opencv.org/4.x/d4/da8/group__imgcodecs.html#ga288b8b3da0892bd651fce07b3bbd3a56)

> **Common Supported Extensions**
>
> - JPEG
> - JPG
> - JPE
> - PNG
> - BMP

### Videos

The supported video fromats by this Python package are limited due to the use of opencv2. The video formats supported are platform dependent, however **avi** and **mp4** video formats have been known to work across multiple platforms.
