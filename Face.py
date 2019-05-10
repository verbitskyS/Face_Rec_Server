import face_recognition
import operator
import numpy as np
import PIL
import io
import base64
resultsArray = {}

def face(base64image, biden_encodingsDict):

    bytes = base64.b64decode(base64image)
    unknown_image = load_face_from_bytes(bytes)
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    for biden_encoding in biden_encodingsDict:
        resultsArray[biden_encoding]=(face_recognition.face_distance([biden_encodingsDict[biden_encoding]], unknown_encoding))
    bestEncondingId = min(resultsArray, key=resultsArray.get)
    return bestEncondingId


def load_face_from_bytes(bytes):
    im = PIL.Image.open(io.BytesIO(bytes))
    mode = "RGB"
    if mode:
        im = im.convert(mode)
    return np.array(im)
