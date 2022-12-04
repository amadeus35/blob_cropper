import cv2
import os
import math


def getDetector():
    # SET UP BLOB DETECTOR
    params = cv2.SimpleBlobDetector_Params()

    params.filterByInertia = False
    params.filterByColor = False
    #params.minThreshold = 10;
    #params.minThreshold = 10;

    # Set Area filtering parameters
    params.filterByArea = True
    params.minArea = 15  # prev 10
    params.maxArea = 150  # 25

    # Set Circularity filtering parameters
    params.filterByCircularity = True
    params.minCircularity = 0.1

    # Set Convexity filtering parameters
    params.filterByConvexity = True
    params.minConvexity = 0.2  # 0.2

    # create blob detector
    return cv2.SimpleBlobDetector_create(params)


def generate_blob_crops(tracking_objects, img, resize=100, output_dir="", frame=0, generateEveryXFrames=30):
    if (frame + 1) % generateEveryXFrames == 0:  # generate for every X frames
        index = 0
        print("Generating crops.. Current Frame = " + str(frame))
        for object_id, tracked_kp_point in tracking_objects.items():
            x, y = tracked_kp_point[0], tracked_kp_point[1]
            x, y = int(x), int(y)
            size = int(tracked_kp_point[2])

            cropped = img[y - size:y + size, x -
                          size:x + size]  # [y1:y2,x1:x2]

            try:
                cropped = cv2.resize(cropped, (resize, resize))
                # cv2_imshow(cropped)
                dir = output_dir + "blob_frame" + \
                    str(frame) + "_" + str(index) + ".png"
                cv2.imwrite(dir, cropped)     # save frame
            except:
                # print("Could not resize img with size" + str(size))
                break
            index += 1


def save_keypoint_img(tracking_objects, img_with_keypoints, show=False, frame_index=0):
    img = img_with_keypoints
    for object_id, point in tracking_objects.items():  # Draw the circle and text around keypoints
        # point[2] is size of keypoint area
        x, y, radius = point[0], point[1], point[2]
        img = cv2.circle(img, (int(x), int(y)),
                         int(radius), (0, 243, 255), 1)
        img = cv2.putText(img, str(object_id), (int(x), int(
            y - 7)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

    if len(tracking_objects) > 0:
        if show == True:
            cv2.imshow(img)  # SHOW IMAGE

        dir = output_dir_imgs + "frame%d.png"
        cv2.imwrite(dir % frame_index, img)
        print("image saved")


def prepare_image(img_name, resize=False, size_x=750, size_y=750):
    if resize == False:
        img = cv2.imread(img_name, 1)
        return img
    else:
        img = cv2.resize(img, (750, 750))
        img = extract_image_center(
            img.copy(),  hcrop=40/2, wcrop=40/2)  # GET CENTER OF IMAGE
        return img

# CROPS PERCENTAGE OF IMAGE WIDTH/HEIGHT WHERE hcrop IS HEIGHT, AND wcrop is WIDTH
# crops based on percentage. For example, hcrop = 20 means crop 20% of the image height, and only leave 80% (600 pixel height)


def extract_image_center(img, hcrop=0, wcrop=10):
    # 750                                                                 wcrop = 20 means crop 20$ of the image width, and only leave 80% (600 pixel width)
    x = img.shape[0]
    y = img.shape[1]  # 750
    xc = int(hcrop*x/100)  # xc = 20 * 750 / 100 = 150
    yc = int(wcrop*y/100)  # yc = 20 * 750 / 100 = 150
    img = img[xc:x-xc, yc:y-yc]  # img[150:600, 150:600] #[y1:y2,x1:x2]
    img = cv2.resize(img, (x, y))
    return img


def generateAnalysisVideo(img_dir, video_dir, total_images):
    # get path to image directory
    image_directory = [os.path.join(img_dir, f) for f in os.listdir(img_dir)]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # codec format
    video_file = video_dir + "video.mp4"
    # get path to video directory
    #video_directory = [os.path.join(video_file,f) for f in os.listdir(video_file)]

    img = []
    for img_name in image_directory:
        img.append(cv2.imread(img_name))

    height, width, layers = img[1].shape
    video = cv2.VideoWriter(video_file, fourcc, 30, (width, height))

    for j in range(0, len(img)):  # create video
        video.write(img[j])

    cv2.destroyAllWindows()
    video.release()


def cropBlobs(videoPath, destinationFolder):
    """
    :param videoPath: Generate images from video and save them to directory
    :param destinationFolder: directory to store output of analysis
    """

    generated_images_dir = destinationFolder + "videoFrames/"
    # "/content/drive/MyDrive/cse485/data/test_videos_output/images/" #output analysis images
    output_dir_imgs = destinationFolder + "analysisImages/"
    # "/content/drive/MyDrive/cse485/data/test_videos_output/video/" #output analysis video
    output_dir_vid = destinationFolder + "analysisVideo/"

    # Target folder where blobs will be written to.
    output_dir_blobCrops = destinationFolder + "blobCrops/"

    video = cv2.VideoCapture(videoPath)
    success, image = video.read()
    count = 0

    while success:
        dir = generated_images_dir + "frame%d.jpg"  # path to save image to
        cv2.imwrite(dir % count, image)     # save frame
        success, image = video.read()
        count += 1

    detector = getDetector()

    # METHOD 01: Get keypoints every frame using blob detector

    frame_index = 0

    # total number of images in directory
    total_image_count = len(os.listdir(generated_images_dir))
    max = total_image_count

    image_directory = [os.path.join(generated_images_dir, f) for f in os.listdir(
        generated_images_dir)]  # get path to image directory


    keypoints = []
    previous_keypoints = []

    track_id = 0
    tracking_objects = {}  # store all tracked blobs
    min_dist = 15  # minimum distance of keypoint to consider a blob as same blob

    max = 90

    for img_name in image_directory:

        if frame_index < max:  # redundant but used to control length of video output

            # prepare_image(img_name, False) #read in image and prepare it
            img = cv2.imread(img_name, 1)
            # get image keypoints using blob detector
            keypoints = detector.detect(img)

            if len(previous_keypoints) > 0:

                if len(tracking_objects) == 0:  # if no tracked objects currently

                    # we cant update when looping, so we need a copy
                    keypoints_copy = list(keypoints).copy()

                    for kp in keypoints_copy:
                        for pkp in previous_keypoints:
                            x1, y1 = kp.pt
                            x2, y2 = pkp.pt
                            distance = math.hypot(x2 - x1, y2 - y1)

                            # WHEN DISTANCE IS < MINIMUM, WE CONSIDER THAT AS THE SAME BLOB, SO WE REMOVE THAT KEYPOINT AND UPDATE THE PREVIOUS KEYPOINT POSITION
                            if distance < min_dist:
                                list(keypoints).remove(kp)
                                continue

                elif len(tracking_objects) > 0:
                    tracking_objects_copy = tracking_objects.copy()
                    keypoints_copy = list(keypoints).copy()

                    for object_id, tracked_kp_point in tracking_objects_copy.items():

                        object_exists = False  # check if saved tracked objects exits. If the distance is small, we can assume that the object exists still. If distance is great, we can assume tracked object is gone / not found

                        for kp in keypoints_copy:  # kp refers to the NEWLY detected keypoints for the frame
                            x1, y1 = kp.pt
                            x2, y2 = tracked_kp_point[0], tracked_kp_point[1]
                            distance = math.hypot(x2 - x1, y2 - y1)

                            # WHEN DISTANCE IS < MINIMUM, WE CONSIDER THAT AS THE SAME BLOB, SO WE REMOVE THAT KEYPOINT AND <<<UPDATE>> THE PREVIOUS KEYPOINT POSITION
                            if distance < min_dist:
                                object_exists = True
                                tracking_objects[object_id] = (kp.pt[0], kp.pt[1], kp.size, tracked_kp_point[3] + 1, tracked_kp_point[4], tracked_kp_point[5], tracked_kp_point[6] +
                                                               kp.size, (tracked_kp_point[6] + kp.size) / (tracked_kp_point[3] + 1))  # Update old point with new point (update position and increment occurence count)

                                if kp in keypoints:  # remove keypoint with small distanc
                                    list(keypoints).remove(kp)
                                    continue

                        # REMOVE KEYPOINTS THAT WERE LOST/NOT FOUND DURING THE CURRENT FRAME
                        if not object_exists:
                            # output_Sheet, row = addSheetRow(outputSheet,row,object_id,tracked_kp_point[4],tracked_kp_point[5],tracked_kp_point[0],tracked_kp_point[1],tracked_kp_point[3], tracked_kp_point[7]) #add row to sheet
                            tracking_objects.pop(object_id)

            for kp in keypoints:  # add any remaining keypoints to tracked objects
                # ADD TRACKED ELEMENT ( Current X, Current Y, KEYPOINT RADIUS, OCCURENCE COUNT, STARTX, STARTY , SUM RADIUS, AVERAGE DIAMETER)
                tracking_objects[track_id] = (
                    kp.pt[0], kp.pt[1], kp.size, 1, kp.pt[0], kp.pt[1], kp.size, kp.size)
                #print("Added ID: %d , Distance between points (%d,%d) and (%d,%d) is: %d" % (track_id, x1,y1,x2,y2 ,distance) )
                track_id += 1

            # REMOVE DUPLICATE KEYPOINTS (SAME X,Y COORDS)
            tracking_objects_copy = tracking_objects.copy()
            for object_id, tracked_kp_point in tracking_objects_copy.items():
                for object_id2, tracked_kp_point2 in tracking_objects_copy.items():
                    x1, y1 = int(tracked_kp_point[0]), int(tracked_kp_point[1])
                    x2, y2 = int(tracked_kp_point2[0]), int(
                        tracked_kp_point2[1])

                    if x1 == x2 and y1 == y2 and object_id != object_id2:
                        # remove duplicate that has least occurences
                        if tracked_kp_point[3] >= tracked_kp_point2[3]:
                            if object_id2 in tracking_objects.keys():
                                # output_Sheet, row = addSheetRow(outputSheet,row,object_id2,tracked_kp_point2[4],tracked_kp_point2[5],tracked_kp_point2[0],tracked_kp_point2[1],tracked_kp_point2[3], tracked_kp_point2[7]) #add row to sheet
                                tracking_objects.pop(object_id2)
                        else:
                            if object_id in tracking_objects.keys():
                                # output_Sheet, row = addSheetRow(outputSheet,row,object_id,tracked_kp_point[4],tracked_kp_point[5],tracked_kp_point[0],tracked_kp_point[1],tracked_kp_point[3], tracked_kp_point[7]) #add row to sheet
                                tracking_objects.pop(object_id)

            # generates the blob crops for this frame
            generate_blob_crops(tracking_objects, img, 100,
                                output_dir_blobCrops, frame_index)

            # Last frame
            # if frame_index >= max - 1:  
            # for object_id, tracked_kp_point in tracking_objects.items():
            #   output_Sheet, row = addSheetRow(outputSheet,row,object_id,tracked_kp_point[4],tracked_kp_point[5],tracked_kp_point[0],tracked_kp_point[1],tracked_kp_point[3], tracked_kp_point[7]) #add row to sheet

            # save image with drawn keypoints for output analysis
            save_keypoint_img(tracking_objects, img, False, frame_index)

            previous_keypoints = list(keypoints).copy()  # make copy of points
            frame_index += 1

            # SAVE OUTPUT ANALYSIS IMAGES


    # CREATE OUTPUT SPREADHSEET
    #wb.save(output_directory +  "output.xls")

    # CREATE ANALYSIS VIDEO
    generateAnalysisVideo(output_dir_imgs, output_dir_vid, max)
