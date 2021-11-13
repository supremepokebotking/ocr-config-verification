# @Author: Dwivedi Chandan
# @Date:   2019-08-05T13:35:05+05:30
# @Email:  chandandwivedi795@gmail.com
# @Last modified by:   Dwivedi Chandan
# @Last modified time: 2019-08-07T11:52:45+05:30


# import the necessary packages
from image_text_processing import *
import numpy as np
import argparse
import time
import cv2
import os
from flask import Flask, request, Response, jsonify
import jsonpickle
#import binascii
import io as StringIO
import base64
from io import BytesIO
import io
import json
from PIL import Image
from flask_cors import CORS
import base64
from flask_restful import inputs

try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3

# construct the argument parse and parse the arguments

confthres = 0.3
nmsthres = 0.1
yolo_path = './'

from image_text_processing import *
# Initialize the Flask application
app = Flask(__name__)
CORS(app)

import os
DEBUG = bool(int(os.environ.get('DEBUG', 1)))
ALLOW_EASY_OCR = bool(int(os.environ.get('ALLOW_EASY_OCR', 0)))
THREADED = bool(int(os.environ.get('THREADED', 1)))
FLASK_PORT = int(os.environ.get('FLASK_PORT', 5111))
os.environ['OMP_THREAD_LIMIT'] = '1'

def get_image_and_params_for_config(request):
    image_section = None

    if request.files is not None and 'image' in request.files:
        img = request.files["image"].read()

        img = Image.open(io.BytesIO(img))
        npimg=np.array(img)
        image=npimg.copy()
        image_section=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

    elif request.get_json() is not None and 'image' in request.get_json():
        base64_string = request.get_json()["image"]

        encoded_data = base64_string.split(',')[1]
        nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
        image_section = cv2.imdecode(nparr, cv2.COLOR_BGR2RGB) # cv2.IMREAD_COLOR in OpenCV 3.1

    params = {}
    raw_params = request.form.to_dict()
    for key in raw_params:
        params[key] = raw_params[key]
    return image_section,params


# route http posts to this method
@app.route('/api/parse_rect_with_pytesseract_config', methods=['POST'])
def rest_parse_rect_with_pytesseract_config():
    image_section, params = get_image_and_params_for_config(request)
    print('params', params)

    ocr_config = json.loads(params['ocr_config'])
    messages = []

    results = []

    always_use_list = False
    if 'always_use_list' in ocr_config:
        always_use_list = ocr_config['always_use_list']

    for language_config in ocr_config['language_configs']:
        # default values
        support_other_langages=False
        psm_7=False
        system_language=None
        language = 'eng'
        game_config = 'pokemon-sword'

        if 'support_other_langages' in language_config:
            support_other_langages=language_config['support_other_langages']
        if 'psm_7' in language_config:
            psm_7=language_config['psm_7']
        if 'language' in language_config:
            system_language=language_config['language']

        text = parse_rect_with_pytesseract(image_section, support_other_langages, psm_7, system_language)
        print('detected text: %s'% text)
        results.append(text)

    if len(results) == 1:
        if not always_use_list:
            return Response(response=json.dumps({"result":results[0]}), status=200,mimetype="application/json")

    return Response(response=json.dumps({"result":results}), status=200,mimetype="application/json")


    # start flask app
if __name__ == '__main__':
    app.run(debug=DEBUG, port=FLASK_PORT, host='0.0.0.0', threaded=THREADED)
