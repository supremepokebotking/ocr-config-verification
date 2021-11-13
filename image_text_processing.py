
import cv2
import pytesseract
import re

try:
    from PIL import Image
except ImportError:
    import Image

import os

ALLOW_EASY_OCR = bool(int(os.environ.get('ALLOW_EASY_OCR', 0)))
if ALLOW_EASY_OCR:
    print('loading easyocr')
    import easyocr
    #reader = easyocr.Reader(['ko','en'])
    reader = easyocr.Reader(['en'])
else:
    print('not going to load easyocr')


def parse_rect_with_pytesseract(image_section, support_other_langages=False, psm_7=False, system_language=None):
    img = Image.fromarray(image_section)
    if support_other_langages and psm_7:
        tess_lang = "jpn+kor+chi_sim"
        if system_language is not None and system_language not in tess_lang:
            tess_lang = '%s+%s' % (system_language, tess_lang)
        raw_text = pytesseract.image_to_string(img, lang=tess_lang, config='--psm 7')
    elif support_other_langages:
        tess_lang = "jpn+kor+chi_sim"
        if system_language is not None and system_language not in tess_lang:
            tess_lang = '%s+%s' % (system_language, tess_lang)
        raw_text = pytesseract.image_to_string(img, lang=tess_lang)
    elif psm_7:
        raw_text = pytesseract.image_to_string(img, config='--psm 7')
    else:
        tess_lang = "eng"
        if system_language is not None and system_language not in tess_lang:
            tess_lang = '%s+%s' % (system_language, tess_lang)
            tess_lang = system_language
        raw_text = pytesseract.image_to_string(img, lang=tess_lang, config='--psm 7')
    raw_text = raw_text.strip()
    return raw_text
