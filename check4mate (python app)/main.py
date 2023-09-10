import cv2
import numpy as np
from roboflow import Roboflow

img = cv2.imread('testTop.png')

# Convert the img to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply edge detection method on the image
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

cv2.imwrite('edges.jpg', edges)

# This returns an array of r and theta values
lines = cv2.HoughLines(edges, 1, np.pi / 180, 150)

linesH, linesV = [], []

# The below for loop runs till r and theta values
# are in the range of the 2d array
# Following loop from geeksforgeeks.com:
for r_theta in lines:
    arr = np.array(r_theta[0], dtype=np.float64)
    r, theta = arr
    # Stores the value of cos(theta) in a
    a = np.cos(theta)

    # Stores the value of sin(theta) in b
    b = np.sin(theta)

    # x0 stores the value rcos(theta)
    x0 = a * r

    # y0 stores the value rsin(theta)
    y0 = b * r

    # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
    x1 = int(x0 + 1000 * (-b))

    # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
    y1 = int(y0 + 1000 * (a))

    # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
    x2 = int(x0 - 1000 * (-b))

    # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
    y2 = int(y0 - 1000 * (a))

    # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
    # (0,0,255) denotes the colour of the line to be
    # drawn. In this case, it is red.

    if abs(x1 - x2) > abs(y1 - y2): #is a horizontal line
        linesH.append([[x1, y1], [x2, y2]])
    else: # is a vertical line
        linesV.append([[x1, y1], [x2, y2]])

    #cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

# All the changes made in the input image are finally
# written on a new image houghlines.jpg

#sort lines greatest to least:
tempH = [[[0, 0], [0, 0]]]
for line in linesH:
    for index, temp in enumerate(tempH):
        if line[0][1] > temp[0][1]:
            if line[0][1] - temp[0][1] < 20: #duplicate line
                break
            tempH.insert(index, line)
            #cv2.line(img, line[0], line[1], (0, 255, 0), 2)
            break
        if temp[0][1] - line[0][1] < 20:  # duplicate line
            break
del tempH[len(tempH)-1] # take out that 0,0,0,0
linesH = tempH

tempV = [[[0, 0], [0, 0]]]
for line in linesV:
    for index, temp in enumerate(tempV):
        if line[0][0] > temp[0][0]:
            if line[0][0] - temp[0][0] < 20: #duplicate line
                break
            tempV.insert(index, line)
            break
        if temp[0][0] - line[0][0] < 20:  # duplicate line
            break
del tempV[len(tempV)-1]
linesV = tempV

while len(linesH) > 9:
    #calculate average distance between lines:
    avg = 0
    for i in range(len(linesH) - 1):
        avg += abs(linesH[i][0][1] - linesH[i+1][0][1])
    avg /= len(linesH)

    if abs(avg - abs(linesH[0][0][1] - linesH[1][0][1])) > abs(avg - abs(linesH[len(linesH)-2][0][1] - linesH[len(linesH)-1][0][1])):
        #if top has more error than bottom
        del linesH[0]
    else:
        del linesH[len(linesH)-1]

while len(linesV) > 9:
    # calculate average distance between lines:
    avg = 0
    for i in range(len(linesV) - 1):
        avg += abs(linesV[i][0][0] - linesV[i + 1][0][0])
    avg /= len(linesV)

    if abs(avg - abs(linesV[0][0][0] - linesV[1][0][0])) > abs(
            avg - abs(linesV[len(linesV) - 2][0][0] - linesV[len(linesV) - 1][0][0])):
        # if top has more error than bottom
        del linesV[0]
    else:
        del linesV[len(linesV) - 1]

for line in linesV+linesH:
    cv2.line(img, line[0], line[1], (255, 0, 0), 2)

cv2.imwrite('linesDetected.jpg', img)


##find intersection points:
for x_line in range(9):
    for y_line in range(9):
        x1 = linesH[x_line][0][0]
        y1 = linesH[x_line][0][1]
        x2 = linesH[x_line][1][0]
        y2 = linesH[x_line][1][1]
        x3 = linesV[y_line][0][0]
        y3 = linesV[y_line][0][1]
        x4 = linesV[y_line][1][0]
        y4 = linesV[y_line][1][1]
        # x_intersect = (((x1*y2)-(y1*x2))*(x3-x4))-((x1-x2)*()) #see wikipedia line-line intersection page

# rf = Roboflow(api_key="vANfmf7pkJ6NiXyLb2wK")
# project = rf.workspace().project("chess-piece-detector-sv3nm")
# model = project.version(2).model
#
# # infer on a local image
# print(model.predict("your_image.jpg").json())
#
# # infer on an image hosted elsewhere
# print(model.predict("URL_OF_YOUR_IMAGE", hosted=True).json())
#
# # save an image annotated with your predictions
# model.predict("your_image.jpg").save("prediction.jpg")