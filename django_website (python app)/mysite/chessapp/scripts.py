import base64
import cv2
import numpy as np

def trim_image(image_text):

    #image_text = image_text[22:]

    image_data = base64.b64decode(image_text)
    nparr = np.frombuffer(image_data, np.uint8)

    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    height, width = image.shape[:2]

    left = int(0.05 * width)
    right = int(width - left)
    top = int(left)
    bottom = int(right)

    cropped_image = image[top:bottom, left:right]

    _, buffer = cv2.imencode('.png', cropped_image)
    cropped_base64_string = base64.b64encode(buffer).decode("utf-8")

    return cropped_base64_string