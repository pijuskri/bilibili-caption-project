import numpy
from paddleocr import PaddleOCR,draw_ocr
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
det_model_dir = "/root/.paddleocr/whl/det/ch/ch_PP-OCRv4_det_infer/"
cls_model_dir = "/root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer/"
rec_model_dir = "/root/.paddleocr/whl/rec/ch/ch_PP-OCRv4_rec_infer/"
ocr = PaddleOCR(use_angle_cls=True, lang='ch', det_model_dir = det_model_dir, cls_model_dir = cls_model_dir, rec_model_dir = rec_model_dir) # need to run only once to download and load model into memory
img_path = './data/test.png'
result = ocr.ocr(img_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)


# draw result
from PIL import Image
result = result[0]
image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path='./data/chinese_cht.ttf')
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')