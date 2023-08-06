# encoding:utf-8
import base64
import requests
from easy_ocr.base import OCR


class XueErSi(OCR):
    """
    https://docai.xueersi.com/books/ai%E6%95%99%E8%82%B2%E5%BC%80%E6%94%BE%E5%B9%B3%E5%8F%B0/page/ocr%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB#1
    """
    url = "http://openapiai.xueersi.com/v1/api/img/ocr/general"
    app_key = "8102b22a5e81e840176d9f381ec6f837"

    def set_app_key(self, key):
        self.app_key = key

    def upload_file(self, filename):
        self.filename = filename

    def get_result(self):
        result = []
        with open(self.filename, "rb") as f:
            data = f.read()
        f_data = base64.b64encode(data)
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
        }
        req_data = {
            "app_key": self.app_key,
            "img": f_data,
            "img_type": "base64"
        }
        try:
            req = requests.post(self.url, data=req_data, headers=headers, timeout=5)
            response = req.json()
        except Exception as e:
            print(e)
        else:
            code = response.get("code")
            if code == 0:
                resp_data = response.get("data", {})
                content = resp_data.get("content", [])
                for c in content:
                    result.append(c.strip())
        return result


def xueersi_ocr(filename, key=None):
    ocr = XueErSi("xueersi")
    ocr.upload_file(filename)
    if key:
        ocr.set_app_key(key)
    return ocr.get_result()
