import argparse
from src.image_processor.image_blobs import cropBlobs
from src.video_processor.video_blobs import cropVideoBlobs
from src.utilities import AppMsg, getFilePaths
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        help='The blob sampler can processes 2 types of media, videos and images.')

    image_parser = subparsers.add_parser(
        'crop_images', description='image_cropper', help='The image cropper analyzes images and crops out their blobs.')

    image_parser.add_argument('-s',
                              '--source', help='The folder path of water samples to be processed.', required=False)
    image_parser.add_argument('-d',
                              '--destination', help='The folder path where the blob samples will be saved to.', required=False)
    image_parser.add_argument('--image_cropper_selected', default='1')

    video_parser = subparsers.add_parser(
        'crop_videos', description='video_cropper', help='The video cropper analyzes videos and crops out their blobs.')

    video_parser.add_argument('-s',
                              '--source', help='The folder path of water samples to be processed.', required=True)
    video_parser.add_argument('-d',
                              '--destination', help='The folder path where the blob samples will be saved to.', required=True)
    video_parser.add_argument('--video_cropper_selected', default='1')

    cmdArgs = parser.parse_args()

    if cmdArgs.video_cropper_selected == '1':
        cropVideoBlobs(cmdArgs.source, cmdArgs.destination)

    # src_folder = cmdArgs.source
    # if not os.path.isdir(src_folder):
    #     AppMsg('Please enter a valid source folder path.')
    #     sys.exit()

    # dest_folder = cmdArgs.destination

    # img_files = getFilePaths(src_folder)

    # for img in img_files:
    #     cropBlobs(dest_folder, img)


if __name__ == '__main__':
    main()
