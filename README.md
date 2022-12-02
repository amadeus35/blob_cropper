# Blob Cropper

A simple module that uses opencv to extract blobs from images. The blob detector used is tuned to target a wide varity of blobs. It attempts to detect circluar blobs, elipse shaped blobs, or blobs with concavity. The extracted blobs are stored in the folder path provided via cmd line interface.

## Python Version Required

3.9.6

## Installation Instructions

1. Clone Repo
2. Using a terminal navigate to root of the project
3. In the terminal execute the command below  
   `pip install -r requirements.txt`

## Application Commands

The application has command line interface with 2 commands.

1. Help command  
   `python ./main.py --help`

2. Crop command  
   `python ./main.py -s folder/path/to/my/images -d folder/path/to/empty/folder`

   > The -s flag's value specifies the folder location of your images  
   > The -d flag's value specifies the folder where you would like the extracted blobs to be saved as image files.
