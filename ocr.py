from PIL import Image
import base64
from io import BytesIO
import cv2
import numpy as np
from paddleocr import PaddleOCR,draw_ocr

from variables import OCR_DEBUG

# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
#det_model_dir = "/root/.paddleocr/whl/det/ch/ch_PP-OCRv4_det_infer/"
#cls_model_dir = "/root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer/"
#rec_model_dir = "/root/.paddleocr/whl/rec/ch/ch_PP-OCRv4_rec_infer/"

#https://pypi.org/project/paddleocr/
ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_space_char=False, show_log=OCR_DEBUG) # need to run only once to download and load model into memory
img_path = './data/test.png'



def perform_ocr(image, debug=False):
    if isinstance(image, str):
        image = Image.open(img_path).convert('RGB')
    image_arr = np.asarray(image)
    if isinstance(image, Image.Image):
        pass
        #buf = BytesIO()
        #rgb = image.convert('RGB')
        #rgb.save(buf, 'jpeg')
        #buf.seek(0)
        #image_bytes = buf.read()
        #data_base64 = str(base64.b64encode(image_bytes),
        #                  encoding="utf-8")
        #image_decode = base64.b64decode(data_base64)
        #img_array = np.frombuffer(image_decode, np.uint8)
        #image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    try:
        result = ocr.ocr(image_arr, cls=False)
    except IndexError: #ignore error for unrecognised character
        return ""
    out_str = ''
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            if debug:
                print(line)
            conf = line[1][1]
            if conf > 0.9:
                out_str = ''.join([out_str, line[1][0]])
    #if len(result) > 0:
    #    out_str = ''.join(result[0][1][0])


    # draw result
    if debug:
        result = result[0]

        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path='./data/chinese_cht.ttf')
        im_show = Image.fromarray(im_show)
        im_show.save('result.jpg')
    return out_str

#if __name__ == '__main__':
perform_ocr(img_path)
print('ocr started')