import os
import io
import cv2
import json
import time
import base64
import jsonpickle
import numpy as np
from PIL import Image
from io import BytesIO
from flask import Flask, request, Response, jsonify


CONFIDENCE_THRESHOLD = 0.3
NON_MAXIMAL_SUPRESSION_THRESHOLD = 0.1
YOLO_PATH = '.'


def get_labels(labels_path):
    label_path=os.path.sep.join([YOLO_PATH, labels_path])
    LABELS = open(label_path).read().strip().split("\n")
    return LABELS

def get_colors(LABELS):
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),dtype="uint8")
    return COLORS

def get_weights(weights_path):
    weights_parent_path = os.path.sep.join([YOLO_PATH, weights_path])
    return weights_parent_path

def get_config(config_path):
    configPath = os.path.sep.join([YOLO_PATH, config_path])
    return configPath

def load_model(configpath,weightspath):
    network = cv2.dnn.readNetFromDarknet(configpath, weightspath)
    return network


def encode_image(image:Image):
  image_to_byte_array = io.BytesIO()
  image.save(image_to_byte_array, format='PNG')
  image_to_byte_array = image_to_byte_array.getvalue()
  encoded_image = base64.encodebytes(image_to_byte_array).decode('ascii')
  return encoded_image


def get_predection(image,network ,LABELS,COLORS):
    (H, W) = image.shape[:2]
    layer_names = network.getLayerNames()
    layer_names = [layer_names[layers - 1] for layers in network.getUnconnectedOutLayers()]
    image_blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    network.setInput(image_blob)
    start_time = time.time()
    layer_outputs = network.forward(layer_names)
    end_time = time.time()
    print("{0} s".format(end_time - start_time))

    boxes = []
    confidences = []
    class_ids = []
    detected_objects = []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > CONFIDENCE_THRESHOLD:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD,
            NON_MAXIMAL_SUPRESSION_THRESHOLD)

    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            color = [int(c) for c in COLORS[class_ids[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            detected_objects.append((LABELS[class_ids[i]], confidences[i]))
            text = "{}: {:.4f}".format(LABELS[class_ids[i]], confidences[i])
            image = cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)
    return image, detected_objects


labels_path = "yolo_weights/coco.names"
cfg_path = "yolo_weights/yolov3.cfg"
weight_path = "yolo_weights/yolov3.weights"
labels = get_labels(labels_path)
CFG = get_config(cfg_path)
weights = get_weights(weight_path)
networks = load_model(CFG, weights)
colors = get_colors(labels)
app = Flask(__name__)


@app.route('/api/v1/detect', methods=['POST'])
def main():
    objects = {}
    image_to_detect_objects = request.files["image"].read()
    image_to_detect_objects = Image.open(io.BytesIO(image_to_detect_objects))
    image_array = np.array(image_to_detect_objects)
    image = image_array.copy()
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    labeled_image, detected_objects = get_predection(image, networks, labels, colors)
    image = cv2.cvtColor(labeled_image, cv2.COLOR_BGR2RGB)
    binary_image = Image.fromarray(image)
    encoded_image = encode_image(binary_image)
    
    for index in detected_objects:
        if index[0] in objects:
            objects[index[0]] += 1
        else:
            objects[index[0]] = 1
    
    response = {
        'labeled_image' : encoded_image,
        'detected_objects' : objects
    }

    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
