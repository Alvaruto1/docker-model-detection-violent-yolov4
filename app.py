import os
from flask import Flask, request, send_from_directory, jsonify, make_response
from flask_cors import CORS, cross_origin
from yolov4.modelo_final_yolo_v4 import detect_objects_in_image
from darknet import *
from werkzeug.utils import secure_filename
from PIL import Image
import base64
from io import BytesIO
import time

UPLOAD_FOLDER = '/model/yolov4/data/images'
DETECTED_FOLDER = '/model/detected_images'
ALLOWED_EXTENSIONS = {'jpeg', 'jpg'}

network, class_names, class_colors = load_network("/model/yolov4/cfg/yolov4-custom.cfg", "/model/yolov4/data/obj.data", "/model/yolov4/data/yolov4-custom_best.weights")


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DETECTED_FOLDER'] = DETECTED_FOLDER
CORS(app)
#cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST','GET'])
def upload_file():    
    if request.method == 'POST':
        download = request.args.get('download')
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
            dict_dectection = detect_objects_in_image(path_save_file, network, class_names, class_colors, thresh=.5, show=download)
            
            #resp.status_code = 200
            resp = jsonify(dict_dectection)
            if download == "True":
                image = Image.open(os.path.join(app.config["DETECTED_FOLDER"], f"detected_{filename}"))
                buffered = BytesIO()
                image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
                resp = jsonify({'status': True, 'detection': dict_dectection, 'imageB64': img_str})
            
            
            #file = send_from_directory(app.config["DETECTED_FOLDER"], f"detected_{filename}", as_attachment=True)
            #response = make_response(file)
            #response.set_cookie('result2', json.dumps(resp))
            return resp
        else:
            return jsonify({'status': False, 'text': "bad file type"})
    else:
        return "no access"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)