import Face
import dataBase
from flask import Flask
from flask import request
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def index():
    db = dataBase.dataBase()
    if request.method == 'POST':
        msg = request.get_data()
        s = msg.decode()
        if "registration" in s:
            try:
                db.add_new(s)
                return "reg"
            except Exception:
                return "error"

        elif "new_face" in s:
            db.add_new_face(id = s.split(" &@# ")[1], image = s.split(" &@# ")[2])
            return "added"
        else:
            try:
                idUser = Face.face(s.split(" &@# ")[1], db.getEncodesDict())
                if(idUser=='no'):
                    return "No user"
            except Exception:
                return "error"
            else:
                s = db.getInfoUserById(idUser)
                print(s)
                return s

    if request.method == 'GET':
        r = request.get_data()
        print(r)
        return "GET"

if __name__ == '__main__':
    app.run(host='localhost', port=5678, threaded=True)









