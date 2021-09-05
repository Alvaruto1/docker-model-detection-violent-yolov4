import os
from flask import Flask, request, redirect, url_for, jsonify
from darknet import *
from werkzeug.utils import secure_filename
from yolov4.modelo_final_yolo_v4 import detect_objects_in_image

UPLOAD_FOLDER = '/model/yolov4/data/images'
ALLOWED_EXTENSIONS = {'jpeg'}

network, class_names, class_colors = load_network("/model/yolov4/cfg/yolov4-custom.cfg", "/model/yolov4/data/obj.data", "/model/yolov4/data/yolov4-custom_best.weights")


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "no file"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return "no file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path_save_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path_save_file)
            resp = jsonify(detect_objects_in_image(path_save_file, network, class_names, class_colors, thresh=.5, show=False))
            resp.status_code = 200
            return resp
        else:
            return "bad file type"
    else:
        return "no access"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)