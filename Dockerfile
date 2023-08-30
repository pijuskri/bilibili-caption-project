FROM paddlecloud/paddleocr:2.6-cpu-latest
RUN pip install "paddleocr>=2.0.1" # Recommend to use version 2.0.1+

#Download models for ocr
ADD https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_det_infer.tar /root/.paddleocr/whl/det/ch/
ADD https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar /root/.paddleocr/whl/cls/
ADD https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_rec_infer.tar /root/.paddleocr/whl/rec/ch/
RUN tar xf /root/.paddleocr/whl/det/ch/ch_PP-OCRv4_det_infer.tar -C /root/.paddleocr/whl/det/ch/
RUN tar xf /root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer.tar -C /root/.paddleocr/whl/cls/
RUN tar xf /root/.paddleocr/whl/rec/ch/ch_PP-OCRv4_rec_infer.tar -C /root/.paddleocr/whl/rec/ch/

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get install python3-tk -y