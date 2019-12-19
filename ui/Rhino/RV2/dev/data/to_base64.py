import os
import base64

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, "00_initialise.png")

with open(FILE, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    print(encoded_string)
