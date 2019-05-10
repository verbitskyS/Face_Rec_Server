import base64
import face_recognition
import os
import numpy as np
import PIL
import io

userData = {}

def getInfoUserById(userId):
    userDataId = userData[userId]
    return userDataId["name"] + " &@# " + userDataId["email"] + " &@# " + userDataId["photo"]

def getEncodesDict():
    encodesDict = {}
    for id in userData:
        encodesDict[id] = userData[id]["encode"]
    return encodesDict

def reg(userInfo): #регистрация нового пользователя ((НУЖНО СДЕЛАТЬ ОЧЕРЕДЬ!!))
    if not userData: #проверка на пустой словарь
        lastId = 0
    else:
        lastId = max(userData.keys()) + 1
    splits = userInfo.split(" &@# ")
    bytes = base64.b64decode(splits[4])
    biden_encoding = face_recognition.face_encodings(load_face_from_bytes(bytes))[0]
    userData[lastId] = {"name": splits[2],"email": splits[3], "photo": splits[4], "encode": biden_encoding}

def load_face_from_bytes(bytes):
    im = PIL.Image.open(io.BytesIO(bytes))
    mode = "RGB"
    if mode:
        im = im.convert(mode)
    return np.array(im)
