#!/usr/bin/env python
# -*-coding:utf-8 -*-
import warnings


def deprecation(message):
    warnings.warn(message, DeprecationWarning, stacklevel=2)


def ocr_image(filename, service="qq"):
    if service == "qq":
        deprecation("QQ OCR have been depecated")
        raise Exception("QQ OCR have been depecated")
    elif service == "xueersi":
        from easy_ocr.xueersi import xueersi_ocr as ocr
    elif service == "baidu":
    	from easy_ocr.baidu import paddle_ocr as ocr
    else:
        from easy_ocr.youdao import youdao_ocr as ocr
    return ocr(filename)
