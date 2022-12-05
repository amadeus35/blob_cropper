import cv2


def init_sheet(outputSheet, row):
    sheet = outputSheet
    newrow = 0
    sheet.write(row, 0, 'Blob ID')
    sheet.write(row, 1, 'Start Position (X,Y)')
    sheet.write(row, 2, 'End Position (X,Y)')
    sheet.write(row, 3, 'Occurences')
    sheet.write(row, 4, 'Average Diameter')
    newrow += 1
    return sheet, newrow

# CREATES ROWS FOR EXCEL SHEET.


def addSheetRow(sheet, row, ID, startX, startY, endX, endY, occurences, avgRadius):
    updatedsheet = sheet
    newrow = row
    updatedsheet.write(row, 0, str(ID))
    updatedsheet.write(row, 1, f'{startX:.1f}' + ", " + f'{startY:.1f}')
    updatedsheet.write(row, 2, f'{endX:.1f}' + ", " + f'{endY:.1f}')
    updatedsheet.write(row, 3, '%d' % occurences)
    # make output limited to 3 decimals
    updatedsheet.write(row, 4, f'{avgRadius:.3f}')
    newrow += 1
    return updatedsheet, newrow


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


def prepare_image(img_name, resize=False, size_x=750, size_y=750):
    if resize == False:
        img = cv2.imread(img_name, 1)
        return img
    else:
        img = cv2.resize(img, (750, 750))
        img = extract_image_center(
            img.copy(),  hcrop=40/2, wcrop=40/2)  # GET CENTER OF IMAGE
        return img
