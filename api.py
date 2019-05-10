import socket
import Face
import dataBase
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
try:
    soc = socket.socket()
    host = "192.168.0.101"
    port = 13134
    soc.bind((host, port))
    soc.listen(500)
    print("all is ok")

    while True:
        conn, addr = soc.accept()
        print("Got connection from", addr)

        s = ''
        msg = conn.recv(10000)
        lenght_of_msg = int(msg.decode().split(" &@# ")[0])
        s += msg.decode()
        while (len(s) < lenght_of_msg):
            msg = conn.recv(10000)
            s += msg.decode()
        print(s)
        if "registration" in s:
            try:
                dataBase.reg(s)
                conn.sendall((s.split(" &@# ")[2] + 'registered!*').encode())
            except Exception:
                conn.sendall("error*".encode())
        else:
            idUser = 0
            try:
                idUser = Face.face(s.split(" &@# ")[1], dataBase.getEncodesDict())
            except Exception:
                conn.sendall(("error*").encode())
            else:
                s = dataBase.getInfoUserById(idUser)
                print(s)
                conn.sendall((s + '*').encode())

except Exception:
    print("error on this server")







