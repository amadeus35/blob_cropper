import os
import cv2
import numpy as np
import math
import uuid
from matplotlib import pyplot as plt
from ..utilities import AppMsg, findRange, Debug, cropSquareSafely, resizeCropSquare
from ..configurations import DEBUG_ON


def setBlobDetector(minArea: int):
    params = cv2.SimpleBlobDetector_Params()

    # Set Area filtering parameters
    params.filterByArea = True
    Debug(f'MinArea: {minArea}')
    params.minArea = minArea
    params.maxArea = minArea * 14

    params.filterByColor = False
    params.blobColor = 0

    params.minDistBetweenBlobs = math.sqrt(minArea)

    # Set Circularity filtering parameters
    params.filterByCircularity = False
    # params.minCircularity = 0

    # Set Convexity filtering parameters
    params.filterByConvexity = True
    params.minConvexity = 0
    params.maxConvexity = 1

    # Set inertia filtering parameters
    params.filterByInertia = True
    params.minInertiaRatio = 0
    params.maxInertiaRatio = 1

    return cv2.SimpleBlobDetector_create(params)


def cropBlobs(folder_path: str, image_path: str):
    """
    The method takes 2 parameter. The first one is the path to the folder where
    the crops will be saved. The second one is a image file path.
    If the folder path does not exist the method will create one with the folder path provided.
    """

    if os.path.isdir(image_path):
        AppMsg('Path is not of file type, skipping entity.')
        return None
    try:
        org_img = cv2.imread(image_path)
        gray_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        height, width = gray_img.shape[:2]
        half_percent = int((height*width)*.5)
        magic_percent = half_percent / 1600
        side_len = int(math.sqrt(magic_percent))
        Debug(f'side_len = {side_len}')

        detector = setBlobDetector(magic_percent)

        flattened_gray_img = gray_img.ravel()

        mean = np.mean(flattened_gray_img)
        std_deviation = np.std(flattened_gray_img)
        left_bound = mean - std_deviation

        new_threshold = left_bound - (std_deviation / 2)
        lum_threshold = left_bound - \
            (std_deviation / 2) if new_threshold > 0 else left_bound
        Debug(f'Initial threshold = {lum_threshold}')
        ret, threshed_img = cv2.threshold(
            gray_img, lum_threshold, 255, cv2.THRESH_BINARY)

        most_keypts_found = []
        most_keypts_found.append(detector.detect(threshed_img))
        most_keypts_found.append(threshed_img)
        most_keypts_found.append(lum_threshold)

        if len(most_keypts_found[0]) == 0:
            most_keypts_found.append(detector.detect(gray_img))
            most_keypts_found.append(gray_img)
            most_keypts_found.append(None)
        if len(most_keypts_found[0]) == 0:
            n = 2
            while lum_threshold < 200:
                if n == 2:
                    lum_threshold = left_bound
                else:
                    lum_threshold = left_bound + n * (std_deviation / 10)
                Debug(f'new_lum_threshold = {lum_threshold}')
                ret, threshed_img = cv2.threshold(
                    gray_img, lum_threshold, 255, cv2.THRESH_BINARY)
                threshed_keypts = detector.detect(threshed_img)
                if len(threshed_keypts) > len(most_keypts_found[0]):
                    most_keypts_found[0] = threshed_keypts
                    most_keypts_found[1] = threshed_img
                    Debug(f'Saving threshold = {lum_threshold}')
                    most_keypts_found[2] = lum_threshold
                n += 2

        threshed_keypts = most_keypts_found[0]
        threshed_img = most_keypts_found[1]
        lum_threshold = most_keypts_found[2]

        Debug(f'Resulting lum_threshold = {lum_threshold}')
        Debug(f'mean = {mean}')

        if DEBUG_ON:
            plt.hist(flattened_gray_img, bins=256, range=[0, 256])
            plt.axvline(mean, color='k', linestyle='dashed', linewidth=1)
            if lum_threshold is not None:
                plt.axvline(lum_threshold, color='blue',
                            linestyle='dashed', linewidth=1)
            plt.axvline(left_bound, color='red',
                        linestyle='dashed', linewidth=1)
            fig = plt.figure(figsize=(10, 7))
            plt.boxplot(flattened_gray_img)

        AppMsg(f'Number of Keypoints found: {len(threshed_keypts)}')
        img_with_keypts = cv2.drawKeypoints(
            threshed_img,
            threshed_keypts,
            np.array([]),
            (0, 0, 255),
            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
        )
        org_with_keypts = cv2.drawKeypoints(
            org_img,
            threshed_keypts,
            np.array([]),
            (0, 0, 255),
            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
        )

        if DEBUG_ON:
            cv2.rectangle(img_with_keypts, (0, 0),
                          (side_len, side_len), (0, 255, 0), 5)

        """
        Crop key points
        """
        # https://www.pythonpool.com/opencv-keypoint/
        crop_on = True
        for keypt in threshed_keypts:
            x_center = keypt.pt[0]
            y_center = keypt.pt[1]
            radius = (keypt.size / 2) * 1.25
            v1 = (int(x_center - radius), int(y_center - radius))
            v2 = (int(x_center + radius), int(y_center + radius))

            v1 = tuple((coord if coord >= 0 else 0 for coord in v1))
            v2 = tuple((coord if coord >= 0 else 0 for coord in v2))

            gray_cropped = gray_img[v1[1]:v2[1], v1[0]:v2[0]]
            flat_gray_img = gray_cropped.ravel()
            range = findRange(flat_gray_img)
            lum_diff = range[1] - range[0]
            Debug(f'crop range = {range}')
            Debug(f'range diff = {lum_diff}')

            if crop_on and DEBUG_ON and lum_diff > 40:
                # https://stackoverflow.com/questions/15589517/how-to-crop-an-image-in-opencv-using-python
                # roi = im[y1:y2, x1:x2]
                gray_cropped = threshed_img[v1[1]:v2[1], v1[0]:v2[0]]
                org_cropped = org_img[v1[1]:v2[1], v1[0]:v2[0]]
                crop_on = False
                file_name = 'cropped-blob-' + str(uuid.uuid4()) + '.png'
                full_path = os.path.join(folder_path, file_name)
                # cv2.imwrite(full_path, cropped)
                cv2.imshow(gray_cropped)
                cv2.imshow(org_cropped)
                cv2.rectangle(img_with_keypts, v1, v2, (255, 0, 0), 5)

            if lum_diff > 40:
                folder_exists = os.path.exists(folder_path)
                if not folder_exists:
                    AppMsg('Output folder does not exist')
                    AppMsg(f'Creating a folder at [{folder_path}]')
                    os.makedirs(folder_path)

                org_cropped = org_img[v1[1]:v2[1], v1[0]:v2[0]]
                file_name = 'cropped-blob-' + str(uuid.uuid4()) + '.png'
                full_path = os.path.join(folder_path, file_name)

                didCrop = cropSquareSafely(full_path, org_cropped)
                new_v1 = v1
                new_v2 = v2
                attempts_left = 30
                while not didCrop and attempts_left > 0:
                    new_rect = resizeCropSquare(
                        (x_center, y_center), new_v1, new_v2)
                    new_v1 = new_rect[0]
                    new_v2 = new_rect[1]
                    org_cropped = org_img[new_v1[1]                                          :new_v2[1], new_v1[0]:new_v2[0]]
                    didCrop = cropSquareSafely(full_path, org_cropped)
                    attempts_left -= 1
                    if didCrop and DEBUG_ON:
                        cv2.rectangle(org_img, new_v1, new_v2, (0, 0, 255), 5)
                if DEBUG_ON:
                    cv2.rectangle(org_img, v1, v2, (255, 0, 0), 5)

        return (org_img, img_with_keypts)
    except:
        AppMsg('An error occurred while processing an image.')
        return None
