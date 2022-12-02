# Blob Cropper

A simple Python module that uses opencv2 to extract 'blobs' from a folder of images. The blob detector used is tuned to target a wide varity of blobs. It attempts to detect circluar blobs, ellipse shaped blobs, or blobs with concavity. The extracted blobs are stored in the folder path provided via the application's CMD line interface.

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

   > The -s flag's value specifies the folder location of your images  
   > The -d flag's value specifies the folder where you would like the extracted blobs to be saved as image files.
