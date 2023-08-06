# encoding:utf-8
import base64
import requests
from easy_ocr.base import OCR


class BaiduPaddle(OCR):
    """
    https://www.paddlepaddle.org.cn/hub/scene/ocr
    """
    url = "https://www.paddlepaddle.org.cn/paddlehub-api/image_classification/chinese_ocr_db_crnn_mobile"

    def upload_file(self, filename):
        self.filename = filename

    def get_result(self):
        result = []
        with open(self.filename, "rb") as f:
            data = f.read()
        f_data = base64.b64encode(data)
        headers = {
            "Content-Type": "application/json",
            "Cookie": "PADDLEID=1a510e7ff1a9094561d6c8b1bc7b6d47",
            "Referer": "https://www.paddlepaddle.org.cn/hub/scene/ocr",
            "Origin": "https://www.paddlepaddle.org.cn",
            "Host": "www.paddlepaddle.org.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
        }
        data = {"image": f_data.decode("utf-8")}
        try:
            req = requests.post(self.url, json=data, headers=headers, timeout=5)
            response = req.json()
        except Exception as e:
            print(e)
        else:
            res = response.get("result", [])
            for r in res:
                d = r.get("data", [])
                for _d in d:
                    v = _d.get("text")
                    if v:
                        result.append(v)
        return result


def paddle_ocr(filename):
    ocr = BaiduPaddle("Paddle")
    ocr.upload_file(filename)
    return ocr.get_result()
