from .configurations import DEBUG_ON
import os
import cv2
import math


def Debug(msg):
    """
    Dynamically prints console statements,
    based on the configuration debug value.
    :param msg:
    :return void:
    """
    if DEBUG_ON == True:
        print(f"[DEBUG]: {msg}")


def AppMsg(msg):
    """
    Prints a formated application message
    """
    print(f"[CROPPER]: {msg}")


def findRange(num_list: list):
    if len(num_list) == 0:
        return None
    elif len(num_list) == 1:
        return (num_list[0], num_list[0])
    else:
        min_val = min(num_list)
        max_val = max(num_list)
        return (min_val, max_val)


def getFilePaths(folder):
    """
    Returns an array of file paths found in given folder
    """
    image_files = []
    for filename in os.listdir(folder):
        image_files.append(folder+'/'+filename)
    return image_files


def resizeCropSquare(center_pt: tuple, rect_v1: tuple, rect_v2: tuple):
    """
    The method will reduce the size of a crop area by 5%
    :param center_pt: The center of the key point
    :param rect_v1: Is the top left vertex of the original crop square
    :param rect_v2: Is the bottom right vertex of the original crop square
    :return tuple: Returns new crop square coordinates 
    """
    x_center = center_pt[0]
    y_center = center_pt[1]
    current_area = (rect_v2[0] - rect_v1[0]) * (rect_v2[1] - rect_v1[1])
    new_area = int(current_area * .95)
    Debug(f'new_area = {new_area}')
    side_len = int(math.sqrt(new_area))
    new_radius = side_len / 2
    new_v1 = (int(x_center - new_radius), int(y_center - new_radius))
    new_v2 = (int(x_center + new_radius), int(y_center + new_radius))
    return (new_v1, new_v2)


def cropSquareSafely(full_path, org_cropped):
    try:
        cv2.imwrite(full_path, org_cropped)
        return True
    except:
        return False
