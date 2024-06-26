# Author: Luca DalCanto | 3/17

import cv2
import numpy as np
import math

from predict import run

import requests
import json

LICHESS_API_TOKEN = 'lip_WbnhfLxNWMD7Z50Rqu0C'

# Functions:
def get_intersection(x1, x2, x3, x4, y1, y2, y3, y4):
    # uses math to find where the intersection of 4 points in space
    # useful for finding the intersection of two lines, each defined by two points
    # or as a way to find the "center" of an irregular quadrilateral
    x_intersect = ((((x1 * y2) - (y1 * x2)) * (x3 - x4)) -
                   ((x1 - x2) * ((x3 * y4) - (y3 * x4)))
                   ) / (((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4)))  # see wikipedia line-line intersection page

    y_intersect = ((((x1 * y2) - (y1 * x2)) * (y3 - y4)) -
                   ((y1 - y2) * ((x3 * y4) - (y3 * x4)))
                   ) / (((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4)))  # see wikipedia line-line intersection page

    return int(x_intersect), int(y_intersect)  # returns a 2D point, (w/ int values)


# ----



def board_to_fen(image, white_turn=True):

    print('startcode')

    img = cv2.imread(image)

    # Convert the img to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply edge detection method on the image
    edges = cv2.blur(gray.copy(), (5,5))
    edges = cv2.Canny(edges, 50, 150, apertureSize=3)

    cv2.imwrite('edges.jpg', edges)

    # This returns an array of r and theta values
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=250)

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
        x1 = int(x0 + 4000 * (-b))
        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
        y1 = int(y0 + 4000 * (a))
        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
        x2 = int(x0 - 4000 * (-b))
        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
        y2 = int(y0 - 4000 * (a))

        #end GfG code

        #Find whether line is closer to horizontal or vertical
        if x1-x2 == 0:
            linesV.append([(x1, y1), (x2, y2)])
        elif abs((y1 - y2) / (x1 - x2)) < 0.2:  # is a horizontal line
            linesH.append([(x1, y1), (x2, y2)])
        elif abs((y1 - y2) / (x1 - x2)) > 1.5:  # is a vertical line
            linesV.append([(x1, y1), (x2, y2)])
        # cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

    # All the changes made in the input image are finally
    # written on a new image houghlines.jpg
    all_lines = img.copy()
    for line in linesV + linesH:
        cv2.line(all_lines, line[0], line[1], (255, 0, 0), 6)
    cv2.imwrite('houghlines.jpg', all_lines)

    # sort lines greatest to least:
    tempH = [[(0, -100), (0, -100)]]
    for line in linesH:
        for index, temp in enumerate(tempH):
            if abs(((temp[0][1] + temp[1][1])/2) -
                   ((line[0][1] + line[1][1])/2)) < 50:  # duplicate line
                break
            if line[0][1] > temp[0][1]:
                tempH.insert(index, line)
                # cv2.line(img, line[0], line[1], (0, 255, 0), 2)
                break

    del tempH[-1]  # take out that 0,0,0,0
    linesH = tempH

    all_lines = img.copy()
    for line in linesH:
        cv2.line(all_lines, line[0], line[1], (255, 0, 0), 10)
    cv2.imwrite('pickedHorizontals.jpg', all_lines)


    tempV = [[(-100, 0), (-100, 0)]]
    for line in linesV:
        for index, temp in enumerate(tempV):
            if abs(((temp[0][0] + temp[1][0])/2) -
                   ((line[0][0] + line[1][0])/2)) < 50:  # duplicate line
                break
            if line[0][0] > temp[0][0]:
                tempV.insert(index, line)
                break
    del tempV[-1]
    linesV = tempV

    all_lines = img.copy()
    for line in linesV:
        cv2.line(all_lines, line[0], line[1], (255, 0, 0), 10)
    cv2.imwrite('pickedVerticals.jpg', all_lines)

    while len(linesH) > 9:
        # calculate average distance between lines:
        avg = 0
        for i in range(len(linesH) - 1):
            avg += abs(linesH[i][0][1] - linesH[i + 1][0][1])
        avg /= len(linesH)

        if abs(avg - abs(linesH[0][0][1] - linesH[1][0][1])) > abs(
                avg - abs(linesH[len(linesH) - 2][0][1] - linesH[len(linesH) - 1][0][1])):
            # if top has more error than bottom
            del linesH[0]
        else:
            del linesH[len(linesH) - 1]


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

    for line in linesV + linesH:
        cv2.line(img, line[0], line[1], (255, 0, 0), 6)

    cv2.imwrite('linesDetected.jpg', img)

    intersection_points = []  # will end up being a 2D list of "2D points" (therefore technically a 3D list)

    ##find intersection points:
    for x_line in range(9):
        intersection_points.append([])  # new row of points
        for y_line in range(9):
            # get 4 points, two from each line:
            x1 = linesH[x_line][0][0]
            y1 = linesH[x_line][0][1]
            x2 = linesH[x_line][1][0]
            y2 = linesH[x_line][1][1]
            x3 = linesV[y_line][0][0]
            y3 = linesV[y_line][0][1]
            x4 = linesV[y_line][1][0]
            y4 = linesV[y_line][1][1]

            # add point to row of points.
            # get_intersection() is a custom function
            # that returns a 2D point

            intersection_points[x_line].append(
                get_intersection(x1, x2, x3, x4, y1, y2, y3, y4))
            cv2.circle(img, intersection_points[x_line][y_line], 10, (0, 0, 255), -1)

    cv2.imwrite('intersections.jpg', img)


    # 0  1  2  3  4  5  6  7
    # 8  9  10 11 12 13 14 15
    # 16 17 18 19 20 21 22 23
    # 24 25 26 27 28 29 30 31
    # 32 33 34 35 36 37 38 39
    # 40 41 42 43 44 45 46 47
    # 48 49 50 51 52 53 54 55
    # 56 57 58 59 60 61 62 63

    # Using intersection points, segment into 64 different images and warp crop them into squares.
    # Then run classification and add to position[] ...

    position = []
    for i in range(64):

        pts1 = np.float32([
            intersection_points[math.floor(i / 8)][i % 8],              # top left
            intersection_points[math.floor(i / 8)][(i % 8) + 1],        # top right
            intersection_points[math.floor(i / 8) + 1][(i % 8)],        # bottom left
            intersection_points[math.floor(i / 8) + 1][(i % 8) + 1]])   # bottom right
        pts2 = np.float32([[224, 224], [0, 224],
                           [224, 0], [0, 0]])

        # Apply Perspective Transform Algorithm
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        cv2.imwrite('imgs/square.jpg', cv2.warpPerspective(gray, matrix, (224, 224)))
        position.append(run(weights='ChessPieceDetector3.pt', source="imgs/square.jpg"))

    #print(position)

    for i, my_dict in enumerate(position):
        if "empty" == my_dict[next(iter(my_dict))]:
            position[i] = "empty"
        if "wp" in my_dict and my_dict["wp"] > 0.02 and ("bp" not in my_dict or my_dict["wp"] > my_dict["bp"]) and (next(iter(my_dict)) == "wp" or my_dict[(next(iter(my_dict)))] < 0.75):
            position[i] = "wp"
        elif "bp" in my_dict and my_dict["bp"] > 0.02 and (next(iter(my_dict)) == "bp" or my_dict[(next(iter(my_dict)))] < 0.75):
            position[i] = "bp"
        else:
            position[i] = next(iter(my_dict))

    #print(position)

    for i, s in enumerate(position):
        if s[0] == 'w':
            position[i] = s[1].upper()
        elif s[0] == 'b':
            position[i] = s[1]

    #print(position)

    fen = ''
    i = 0
    j = 0
    while i < 8: #current row
        for k in range(8-j):
            if position[(8*i)+j+k] != 'empty':
                if k != 0:
                    fen += str(k)
                fen += position[(8*i)+j+k]
                j += k + 1
                break
            if j+k == 7:
                fen += str(1 + k)
                j = 8
        if j == 8:
            fen += '/'
            j = 0
            i += 1

    if(white_turn):
        fen += ' w'
    else:
        fen += ' b'

    fen += ' - - 10 10'
    return fen


#engine = chess.engine.SimpleEngine.popen_uci("usr/local/Cellar/stockfish/")
# board = chess.Board(board_to_fen('board3.JPG'))
# print(board)

def get_fen(image):
    return board_to_fen(image=image)

# fish = stockfish.Stockfish(path="/usr/local/Cellar/stockfish")

def run_analysis(fen):
    url = 'https://lichess.org/api/cloud-eval'
    headers = {
        'Authorization': f'Bearer {LICHESS_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    params = {
        'fen': fen,
        'multiPv': 1,
        'depth': 15
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        best_moves = data.get('pvs', [])
        return best_moves
    else:
        raise Exception(f"Error fetching analysis: {response.status_code} {response.text}")

# try:
#     best_moves = run_analysis('rnbqkbnr/1ppp1pp1/p6p/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 4')
#     print(best_moves)
# except Exception as e:
#     print(e)