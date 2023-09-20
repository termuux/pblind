ext_determiner = {
    'args': {
                "stop_words": None,
                "lowercase": True,
                "norm": 'l1',
                "use_idf": False,
            },
    'sensitivity': 0.2,

}


google_speech = {

    'lang': "en"
}


# Object Detection 

stream_source = 0
config_path = '/var/pool/sys/fs/home/azine/dist/projects/pblind/src/dyno/extensions/marketplace/dobject/dnn/ssd.pbtxt'
weights_path = '/var/pool/sys/fs/home/azine/dist/projects/pblind/src/dyno/extensions/marketplace/dobject/dnn/frozen.pb'
class_names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'street sign', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'hat', 'backpack', 'umbrella', 'shoe', 'eye glasses', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'plate', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'mirror', 'dining table', 'window', 'desk', 'toilet', 'door', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'blender', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush', 'hair brush']
confidence_threshold = 0.6      
time_to_detect_objects = 50


# Opitcal Character Recognition Parameters

tesseract_path = '/usr/bin/tesseract'
crop_size = [500,500]
view_mode = 1
stream_source = 0
time_to_run = 30

# Open weather map confgurations


OPEN_WEATHER_MAP_CONFIG = {
    'unit': 'celsius',
    'key':  'f45192f86e99294305192beccdb5a3d8',
    'city_id': 1283617
}

# Camera file

camera_file = '<video0>'
object_detection_url = 'https://secure-wave-43014.herokuapp.com/api/v1/detect'
time_to_show_image = 10000
