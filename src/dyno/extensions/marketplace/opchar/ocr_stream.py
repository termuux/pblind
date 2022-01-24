import threading
from dyno.config import tesseract_path, crop_size, view_mode, stream_source, time_to_run
from dyno.extensions.marketplace.opchar.optical.optical_root import ocr_stream, tesseract_location
from dyno.extensions.extension import ParentExtension

class OpticalCharacterStream(ParentExtension):
    @classmethod
    def optical_character_stream(cls, **kwargs):
        cls.response('Starting Live Text Detection Stream')
        tesseract_location(tesseract_path)
        extracted_text = ocr_stream(cls, crop_size, time_to_run, stream_source, view_mode, language=None)
        longest_text = max(extracted_text, key=len)
        try:
            cls.response(longest_text)
            cls.console(longest_text)
        except ValueError:
            cls.response('Cant detect text. Try running long stream detection')
            cls.console(""" Cant extract text. Hints:
            1. Improve lighting conditions.
            2. Call longer stream detection function.
            3. Hold the text document steadily.""")
