import base64
import face_recognition
import os
import numpy as np
import PIL
import io
import sqlite3

class dataBase:
    cursor = None
    conn = None
    count = None
    def __init__(self):
        self.conn = sqlite3.connect("mydatabase.db")
        self.cursor = self.conn.cursor()

    def create(self):
        self.cursor.execute("""CREATE TABLE users
                            (id integer, name text, email text,
                            photos text, encode text)
                            """)

    def add_new(self, userInfo):
        count = """SELECT count(*) as tot FROM users"""
        self.cursor.execute(count)
        self.count = self.cursor.fetchone()[0]
        print(self.count)
        print(type(self.count))
        lastid = self.count
        splits = userInfo.split(" &@# ")
        bytes = base64.b64decode(splits[4]) #С„РѕС‚Рѕ РІ Р±Р°Р№С‚Р°С…
        biden_encoding = face_recognition.face_encodings(load_face_from_bytes(bytes))[0] #СЃРѕС…СЂР°РЅСЏРµРј РµС‰Рµ СЌРЅРєРѕРґ, С‡С‚РѕР±С‹ РїРѕСЃС‚РѕСЏРЅРЅРѕ РЅРµ СЌРЅРєРѕРґРёСЂРѕРІР°С‚СЊ СЃРѕС…СЂР°РЅРµРЅРЅС‹Рµ С„РѕС‚РѕРіСЂР°С„РёРё
        enc_str = ""
        for i in biden_encoding:
            enc_str += str(i) + " "
        tuple_str = (lastid, splits[2], splits[3], splits[4], enc_str[:-1])
        self.cursor.execute("INSERT INTO users VALUES (?,?,?,?,?)", tuple_str)
        self.conn.commit()

    def getInfoUserById(self, id):
        self.cursor.execute("SELECT * FROM users WHERE id=?", [(id)])
        g = self.cursor.fetchone()
        photos = g[3].split(" /*(=)*\ ")
        return str(g[0]) +" &@# "+ g[1] + " &@# " + g[2] + " &@# " + photos[0]

    def getEncodesDict(self):
        count = """SELECT count(*) as tot FROM users"""
        self.cursor.execute(count)
        self.count = self.cursor.fetchone()[0]
        encodesDict = {}
        sql = "SELECT encode FROM users"
        self.cursor.execute(sql)
        g = self.cursor.fetchall()
        for i in range(self.count):
            splits = g[i][0].split(" /*(=)*\ ")
            enc = []
            for j in range(len(splits)):
                enc.append(np.array(splits[j].split(" ")).astype(float).tolist())
                encodesDict[i] = enc
        return encodesDict

    def add_new_face(self, id, image):
        count = """SELECT count(*) as tot FROM users"""
        self.cursor.execute(count)
        self.count = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT * FROM users WHERE id=?", [(id)])
        g = self.cursor.fetchone()
        bytes = base64.b64decode(image)  # С„РѕС‚Рѕ РІ Р±Р°Р№С‚Р°С…
        biden_encoding = face_recognition.face_encodings(load_face_from_bytes(bytes))[0]  # СЃРѕС…СЂР°РЅСЏРµРј РµС‰Рµ СЌРЅРєРѕРґ, С‡С‚РѕР±С‹ РїРѕСЃС‚РѕСЏРЅРЅРѕ РЅРµ СЌРЅРєРѕРґРёСЂРѕРІР°С‚СЊ СЃРѕС…СЂР°РЅРµРЅРЅС‹Рµ С„РѕС‚РѕРіСЂР°С„РёРё
        enc_str = ""
        for i in biden_encoding:
            enc_str += str(i) + " "
        newg3 = g[3] + " /*(=)*\ " + image
        newg4 = g[4] + " /*(=)*\ " + enc_str[:-1]
        sql = """
              UPDATE users
              SET photos =? 
              WHERE id =?
              """
        self.cursor.execute(sql, [(newg3), (id)])
        sql = """
              UPDATE users
              SET encode =? 
              WHERE id =?
              """
        self.cursor.execute(sql, [(newg4), (id)])
        self.conn.commit()

def load_face_from_bytes(bytes):
    im = PIL.Image.open(io.BytesIO(bytes))
    mode = "RGB"
    if mode:
        im = im.convert(mode)
    return np.array(im)