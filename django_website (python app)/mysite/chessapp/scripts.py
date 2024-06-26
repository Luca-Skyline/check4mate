import base64
import cv2
import numpy as np
from PIL import Image
import io

def trim_image(image_data):

    nparr = np.frombuffer(image_data, np.uint8)

    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    height, width = image.shape[:2]

    left = int(0.05 * width)
    right = int(0.95 * width)
    top = int(0.05 * width) + 12
    bottom = top + int(0.90 * width)

    cropped_image = image[top:bottom, left:right]

    _, buffer = cv2.imencode('.png', cropped_image)
    cropped_base64_string = base64.b64encode(buffer).decode("utf-8")

    return cropped_base64_string