import os
import io
import json
import time
import base64
import easyocr
import threading
import random
from PIL import Image
from PIL import ImageDraw
from io import BytesIO
from flask import Flask, request, Response, jsonify

response = {  }
models_path = '/app/models/'
os.environ['EASYOCR_MODULE_PATH'] = models_path 
image_to_detect_text = None

def generate_random_hash():
    return random.getrandbits(128) 


def recognize_text(image):
    print('[+] Recognizing text.')
    reader = easyocr.Reader(['en'], gpu=False, model_storage_directory=models_path, download_enabled=False)
    result = reader.readtext(image, detail=1)
    return result

def draw_boxes(image, easyocr_output, color='yellow', width=2):
    print('[+] Drawing box.')
    draw = ImageDraw.Draw(image)
    for bound in easyocr_output: 
        p0, p1, p2, p3 = bound[0] 
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    return image

def extract_text(easyocr_output):
    print('[+] Extracting text')
    extracted_text = ''
    for bound in easyocr_output:
        extracted_text += bound[1] + ' '
    return extracted_text

def encode_image(image:Image):
    print('[+] Encoding image')
    image_to_byte_array = io.BytesIO()
    image.save(image_to_byte_array, format='PNG')
    image_to_byte_array = image_to_byte_array.getvalue()
    encoded_image = base64.encodebytes(image_to_byte_array).decode('ascii')
    return encoded_image

def start_ocr():
    global reponse
    easyocr_output = recognize_text(image_to_detect_text)
    extracted_text = extract_text(easyocr_output)
    bounded_image = draw_boxes(image_to_detect_text, easyocr_output)
    bounded_image = encode_image(bounded_image)
    response = {
        'bounded_image': bounded_image,
        'detected_text' : extracted_text
    }
    print('[+] OCR done.')

app = Flask(__name__)


@app.route('/api/v1/tdetect', methods=['POST'])
def main():
    global image_to_detect_text
    image_to_detect_text = request.files["image"].read()
    ocr_thread = threading.Thread(target=start_ocr)
    ocr_thread.start()
    reponse = {
            'message' : 'OCR detection started. Get results at /api/v1/tget after some time.',
            'key' : '12345'
            } 
    return jsonify(response)

@app.route('/api/v1/tget', methods=['POST'])
def get_text():
    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
