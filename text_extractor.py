from PIL import Image
from pytesseract import pytesseract
import io
import cv2
from text_augmentor import augmentor
from collections import Counter

class extractor:
    def __init__(self):
        self.ptT = "C:/Tesseract-OCR/tesseract.exe"

    def extract_text(self, img):
        try:
            l = cv2.resize(img, (300, 500))
            
            img = Image.fromarray(img)

            pytesseract.tesseract_cmd = self.ptT
            # img = augmentor.sharpen(img)
            text = pytesseract.image_to_string(img)
            return text
        except:
            pass