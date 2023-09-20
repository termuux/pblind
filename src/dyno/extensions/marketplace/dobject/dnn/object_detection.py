import os
import io
import cv2
import time
import json
import base64
import imageio
import requests
import threading
import tempfile
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime, timedelta
from dyno.tools.connection import check_connection
from dyno.extensions.extension import ParentExtension
from dyno.extensions.marketplace.music.youtube.downloader import make_download_directory, remove_download_directory
from dyno.config import stream_source, config_path, weights_path, class_names, confidence_threshold, time_to_detect_objects, camera_file, object_detection_url, time_to_show_image

def detect_objects_online(class_instance):
    temporary_dir = make_download_directory()
    camera = imageio.get_reader(camera_file)

    time.sleep(1)
    
    image = camera.get_data(0)
    
    camera.close()
    
    post_path = os.path.join(temporary_dir.name, 'post.png')
    get_path = os.path.join(temporary_dir.name, 'get.png')
    
    imageio.imwrite(post_path, image, format='PNG')
    
    files = {
        'image' : ('post.png', open(post_path, 'rb')),
    }
    
    response_string = requests.post(object_detection_url, files=files).text
    response_string = json.loads(response_string)
    response_image = response_string['labeled_image']
    response_image = base64.b64decode(response_image)
    
    with open(get_path, 'wb') as write_file:
        write_file.write(response_image)
    
    response_string = response_string['detected_objects']
    objects_string = ''
    
    try:
        for objects in response_string:
            objects_string += str(response_string[objects]) + ' ' + objects
    except Exception as e:
        class_instance.console('Exception : {0}'.format(e))
    
    if len(objects_string) > 2:
        class_instance.response('{0} were detected around you'.format(objects_string))
        try:
            root_window = tk.Tk()
            image = ImageTk.PhotoImage(Image.open(get_path))
            label = tk.Label(root_window, image=image).pack()
            root_window.after(time_to_show_image, lambda: root_window.destroy())
            root_window.mainloop()
        except:
            pass
    else:
        class_instance.response('Couldnot detect any objects')


def detect_objects_offline(class_instance):
    objects_string = ''
    stream = cv2.VideoCapture(stream_source)
    network  = cv2.dnn_DetectionModel(weights_path, config_path)
    network.setInputSize(320,320)
    network.setInputScale(1.0/ 127.5)
    network.setInputMean((127.5, 127.5, 127.5))
    network.setInputSwapRB(True)
    captured_objects = {}
    detection_end_time = datetime.now() + timedelta(seconds=time_to_detect_objects)

    while True:
        success, frame = stream.read()
        class_ids, confidence, bounding_box = network.detect(frame, confThreshold=confidence_threshold)
        pressed_key = cv2.waitKey(1) & 0xFF
        if pressed_key == ord('q') or (datetime.now() > detection_end_time):
            break

        if len(class_ids) !=0 :
            for class_id, conf, box in zip(class_ids.flatten(), confidence.flatten(), bounding_box):
                cv2.rectangle(frame, box, color=(255,0,0))
                detected_object = class_names[class_id - 1]
                cv2.putText(frame, detected_object,(box[0] + 200 , box[1] + 30), cv2.FONT_HERSHEY_SIMPLEX,1, (255,255,255),1)

            if detected_object not in captured_objects:
                captured_objects[detected_object] = 1
            elif detected_object in captured_objects:
                captured_objects[detected_object] += 1
        try:
            cv2.imshow('Object Detection Stream', frame)
        except:
            pass

    objects = [*captured_objects]
    for object in captured_objects:
        if captured_objects[object] > 5:
            objects_string += object + ' ' 
    
    if len(objects_string) > 2:
        class_instance.response('{0} are around you'.format(objects_string))
    else:
        class_instance.response('Could not detect any objects around you')


class ObjectDetector(ParentExtension):
    
    @classmethod
    def detect_objects(cls, **kwargs):
       online_detection = threading.Thread(target=detect_objects_online, args=(cls,))
       offline_detection = threading.Thread(target=detect_objects_online, args=(cls,))
       if check_connection():
           try:
               online_detection.start()
           except:
               offline_detection.start()
       else:
           offline_detection.start()
