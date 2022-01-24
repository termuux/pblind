import os
import sys
import cv2
import time
import numpy
import datetime
import threading
import pytesseract
from pathlib import Path
from threading import Thread
from datetime import datetime, timedelta

def tesseract_location(root_path):
    try:
        pytesseract.pytesseract_cmd = root_path
    except FileNotFoundError:
        print('Tesseract not found.')
        

class RateCounter:

    def __init__(self):
        self.start_time = None
        self.iterations = 0

    def start_counter(self):
        self.start_time = time.perf_counter()
        return self

    def increase_iterations(self):
        self.iterations += 1

    def show_rate(self):
        elapsed_time = (time.perf_counter() - self.start_time)
        return self.iterations / elapsed_time

    

class VideoStream:
    def __init__(self, stream_source=0):
        self.stream = cv2.VideoCapture(stream_source)
        (self.is_grabbed, self.frame) = self.stream.read()
        self.is_stopped = False

    def start_thread(self):
        Thread(target=self.get_frames, args=()).start()
        return self
    
    def get_frames(self):
        while not self.is_stopped:
            (self.is_grabbed, self.frame) = self.stream.read()
        
    def get_stream_dimensions(self):
        width = self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return int(width), int(height)

    def stop_thread(self):
        self.is_stopped = True

class OpticalCharacterRecognizer:
    def __init__(self):
        self.boxes = None
        self.is_stopped = False
        self.exchange_frames = None
        self.language = None
        self.width = None
        self.height = None
        self.crop_width = None
        self.crop_height = None

    def start_process(self):
        Thread(target=self.optical_character_recognizer, args=()).start()
        return self

    def set_exchange(self, video_stream):
        self.exchange_frames = video_stream
    
    def set_language(self, language):
        self.language = language

    

    def optical_character_recognizer(self):
        while not self.is_stopped:
            if self.exchange_frames is not None:
                frame = self.exchange_frames.frame
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                frame = frame[self.crop_height:(self.height - self.crop_height),
                          self.crop_width:(self.width - self.crop_width)]
                self.boxes = pytesseract.image_to_data(frame, lang=self.language)
        
    def set_dimensions(self, width, height, crop_width, crop_height):
        self.width = width
        self.height = height
        self.crop_width = crop_width
        self.crop_height = crop_height

    def stop_process(self):
        self.is_stopped = True

def capture_image(frame, captures=0):
    current_time = datetime.datetime.now()
    file_name = 'ocr_' + now.strfttime('%Y_%m_%d') + str(captures + 1) + '.jpg'
    parent_path = os.path.join('build', 'ocr_images')
    Path(parent_path).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(parent_path, file_name)
    cv2.imwrite(file_path, frame)
    captures += 1
    return captures 

def view_modes(mode: int, confidence: int):
    confidence_threshold = None
    color = None
    
    if mode == 1:
        confidence_threshold = 75
        color = (0, 255, 0)

    if mode == 2:
        confidence_threshold = 0
        if confidence >= 50:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)
        
    if mode == 3:
        confidence_threshold = 0
        color = (int(confidence) * 2.55, int(confidence) * 2.55, 0)

    if mode ==  4:
        confidence_threshold = 0
        color = (0, 0, 255)

    return confidence_threshold, color

def put_ocr_boxes(boxes, frame, height, crop_width=0, crop_height=0, view_mode=1):
    if view_mode not in [1, 2, 3, 4]:
        raise Exception('View mode is invalid')

    text = ''
    if boxes is not None:
        for index,box in enumerate(boxes.splitlines()):
            box = box.split()
            if index != 0:
                if len(box) == 12:
                    x, y, w, h = int(box[6]), int(box[7]), int(box[8]), int(box[9])
                    confidence = box[10]
                    word = box[11]
                    x += crop_width
                    y += crop_height

                    confidence_threshold, color = view_modes(view_mode, int(confidence))

                    if int(confidence) > confidence_threshold:
                        cv2.rectangle(frame, (x,y), (w+x, h+y), color, thickness=1)
                        text = text + ' ' + word
                
        if text.isascii() and len(text) > 2:
            cv2.putText(frame, text, (5, height -5), cv2.FONT_HERSHEY_PLAIN, 1, (200, 200, 200))
            return frame, text

    return frame, None

def put_crop_box(frame: numpy.ndarray, width: int, height: int, crop_width: int, crop_height: int):
    cv2.rectangle(frame, (crop_width, crop_height), (width - crop_width, height - crop_height),
    (255,233,0), thickness=1)
    return frame

def put_rate(frame: numpy.ndarray, rate: float) -> numpy.ndarray:
    cv2.putText(frame, 'fps: '.format(int(rate)),
    (10,35), cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 145, 255))
    return frame

def put_language(frame: numpy.ndarray, language_string: str) -> numpy.ndarray:
    cv2.putText(frame, language_string,
            (10, 65), cv2.FONT_HERSHEY_DUPLEX, 1.0 , (255, 45, 25))
    return frame

def ocr_stream(extension_class, crop: list[int, int],time_to_run: int = 10, source: int = 0, view_mode: int =1 , language=None):
    captures = 0
    captured_text = []
    end_time = datetime.now() + timedelta(seconds=time_to_run)
    video_stream = VideoStream(source).start_thread()
    image_width, image_height = video_stream.get_stream_dimensions()

    if crop is None:
        crop_x, crop_y = (200, 200)
    else:
        crop_x, crop_y = crop[0], crop[1]
        if crop_x > image_width or crop_y > image_height or crop_x < 0 or crop_y < 0:
            crop_x, crop_y = 0, 0
            print('Invalid crop dimensions.')
    
    optical_character = OpticalCharacterRecognizer().start_process()
    print('Starting Optical Character Recognition Live Stream')
    print('Active threads are : {}'.format(threading.activeCount()))
    optical_character.set_exchange(video_stream)
    optical_character.set_language(language)
    optical_character.set_dimensions(image_width, image_height, crop_x, crop_y)

    capsule_alpha = RateCounter()
    capsule_alpha.start_counter()
    lang_name = 'English'

    print('Press x to capture image.')
    print('Press q to quit stream.')

    while True:
        pressed_key = cv2.waitKey(1) & 0xFF
        if pressed_key == ord('q') or (datetime.now() > end_time):
            video_stream.stop_thread()
            optical_character.stop_process()
            print('Stopping Optical Character Recognition Stream ')
            print('{} images were captured'.format(captures))
            return captured_text
            break

        frame = video_stream.frame
        frame = put_crop_box(frame, image_width, image_height, crop_x, crop_y)
        frame, text = put_ocr_boxes(optical_character.boxes,frame, image_height, crop_width=crop_x, crop_height=crop_y, view_mode=view_mode)
        
        if text is not None and text not in captured_text:
           captured_text.append(text) 
        
        if pressed_key == ord('x'):
            print('Capturing image '+ text)
            captures = capture_image(frame, captures)
        
        cv2.imshow('Optical Character Recognizer Stream', frame)
        capsule_alpha.increase_iterations()
        



