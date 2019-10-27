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
        if len(biden_encodingsDict[biden_encoding]) != 128:
            res = 1
            for i in range(len(biden_encodingsDict[biden_encoding])):
                res_prom = face_recognition.face_distance([biden_encodingsDict[biden_encoding][i]], unknown_encoding)
                if (res_prom < res):
                    res = res_prom
            resultsArray[biden_encoding] = res
        else:
            resultsArray[biden_encoding] = (
                face_recognition.face_distance([biden_encodingsDict[biden_encoding]], unknown_encoding))
    bestEncondingId = min(resultsArray, key=resultsArray.get)
    print(min(resultsArray.values()))
    if min(resultsArray.values()) > 0.5:
        return 'no'
    else:
        return bestEncondingId


def load_face_from_bytes(bytes):
    im = PIL.Image.open(io.BytesIO(bytes))
    mode = "RGB"
    if mode:
        im = im.convert(mode)
    return np.array(im)
