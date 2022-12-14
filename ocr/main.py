import io
import logging

from fastapi import FastAPI, APIRouter, Request, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

import PIL
from PIL import Image, ImageOps

import urllib
import numpy as np
import cv2
import easyocr
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'easyocr_vdt');
reader = easyocr.Reader(['en'], gpu=False)

app = FastAPI()
router = APIRouter()
reader = easyocr.Reader(["ko","en"])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ocr")

def url_to_image(url):
    """
    download the image, convert it to a NumPy array, and then read it into OpenCV format
    :param url: url to the image
    :return: image in format of Opencv
    """
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    print("url = ", url)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def data_process(data):
    """
    read params from the received data
    :param data: in json format
    :return: params for image processing
    """
    image_url = data["image_url"]
    secret_key = data["secret_key"]

    return url_to_image(image_url), secret_key


def recognition(image):
    """
    :param image:
    :return:
    """
    results = []
    texts = reader.readtext(image)
    for (bbox, text, prob) in texts:
        output = {
            "coordinate": [list(map(float, coordinate)) for coordinate in bbox],
            "text": text,
            "score": prob
        }
        results.append(output)

    return results

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.route('/ocr', methods=['GET', 'POST'])
def process():
    """
    received request from client and process the image
    :return: dict of width and points
    """
    data = request.get_json()
    image, secret_key = data_process(data)
    if secret_key == SECRET_KEY:
        results = recognition(image)
        return {
            "results": results
        }
    else:
        return {"error": "NOT Found SECRET_KEY"}

# # @router.post("/ocr")
# @app.post("/ocr")
# async def do_ocr(request: Request, file: UploadFile = File(...)):
#     if file is not None:
#         # res = ocr.readtext(await file.read())
#         # res = ocr.readtext(file.file)
#         # via pil
#         imgFile = np.array(PIL.Image.open(file.file).convert("RGB"))
#         res = reader.readtext(imgFile)

#         # return array of strings
#         return [item[1] for item in res]
#         # probable_text = "\n".join((item[1] for item in res))
#         # return StreamingResponse(
#         #     io.BytesIO(probable_text.encode()), media_type="text/plain"
#         # )

#     return {"error": "missing file"}


# @app.post("/ocr_form")
# async def do_ocr_form(request: Request, file: UploadFile = File(...)):
#     # form = await request.form()
#     # file = form.get("file", None)
#     if file is not None:
#         # res = ocr.readtext(await file.read())
#         res = reader.readtext(file.file.read())
#         return [item[1] for item in res]

#     return {"error": "missing file"}


app.include_router(router)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)