# Blob Cropper

A simple Python module that uses opencv2 to extract 'blobs' from a folder of images. The blob detector used is tuned to target a wide varity of blobs. It attempts to detect circluar blobs, ellipse shaped blobs, or blobs with concavity. The extracted blobs are stored as PNG files in the folder path provided via the application's CMD line interface.

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

The application has command line interface with 2 commands.

1. Help command  
   `python ./main.py --help`

2. Crop command  
   `python ./main.py -s folder/path/to/my/images -d folder/path/to/empty/folder`

   > The -s flag's value specifies the source folder where images will be retrieved from and processed.  
   > The -d flag's value specifies the destination folder where the extracted blobs will be saved as image files.  
   > &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_If destination folder does not exist one will be created inside the source folder._

## Limitations

The images processed by the module must have extensions supported by opencv2.  
A listing of supported opencv2 image extensions can be found in the [opencv2 docs](https://docs.opencv.org/4.x/d4/da8/group__imgcodecs.html#ga288b8b3da0892bd651fce07b3bbd3a56)

> **Common Supported Extensions**
>
> - JPEG
> - JPG
> - JPE
> - PNG
> - BMP
