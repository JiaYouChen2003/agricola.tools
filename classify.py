import pytesseract
from PIL import Image\

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def imgclassify(img):
    data = pytesseract.image_to_data(img, output_type='dict')
    boxes = len(data['level'])

    for i in range(boxes):
        if data['text'][i] != '':
            print(data['text'][i])