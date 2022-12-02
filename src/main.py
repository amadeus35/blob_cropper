import argparse
from crop_blobs import getFilePaths, cropBlobs
from utilities import AppMsg
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s',
                        '--source', help='The folder path of water samples to be processed.')
    parser.add_argument('-d',
                        '--destination', help='The folder path where the blob samples will be saved to.')

    cmdArgs = parser.parse_args()

    src_folder = cmdArgs.source
    if not os.path.isdir(src_folder):
        AppMsg('Please enter a valid source folder path.')
        sys.exit()

    dest_folder = cmdArgs.destination

    img_files = getFilePaths(src_folder)

    for img in img_files:
        org_img, thresh_img = cropBlobs(dest_folder, img)


if __name__ == '__main__':
    main()
