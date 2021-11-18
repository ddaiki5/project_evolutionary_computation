#coding: UTF-8
#refer: https://qiita.com/onaka_yurusugi/items/7fe2bacb7ede88eadd1b
#refer: https://rightcode.co.jp/blog/information-technology/python-tesseract-image-processing-ocr
import sys
import os

import pyocr
import pyocr.builders
import pyautogui

from PIL import Image
from time import sleep, time

'''
事前にTesseractのインストールが必要　
referを参照
'''
TESSERACT_PATH = 'C:\Program Files\Tesseract-OCR'  # 事前にダウンロード
os.environ["PATH"] += os.pathsep + TESSERACT_PATH

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)

tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))

def get_pos():
    '''docstring
    pyautoguiを使用してスクリーンショットのための座標の取得\n
    ３秒ごとに左上と右下の座標を取得する
    '''

    # 3秒待ってからカーソル位置の座標を取得
    print("左上隅の座標を取得します")
    sleep(3)
    x1, y1 = pyautogui.position()
    print(str(x1) + "," + str(y1))

    # 3秒待ってからカーソル位置の座標を取得
    print("右下隅の座標を取得します")
    sleep(3)
    x2, y2 = pyautogui.position()
    print(str(x2) + "," + str(y2))

    # PyAutoGuiのregionの仕様のため、相対座標を求める
    x2 -= x1
    y2 -= y1

    return(x1, y1, x2, y2)

def screen_shot(x1, y1, x2, y2):
    '''docstring
    pyautoguiを使用して指定した場所のスクリーンショットを取得して保存する
    '''
    sc = pyautogui.screenshot(region=(x1, y1, x2, y2))  # get_pos関数で取得した座標を使用
    sc.save('tmp/ocr_actor.jpg')

def ocr_actors():
    '''docstring
    保存した画像から文字認識を行う\n
    現状認識した文字をすべて表示している
    '''
    txt = tool.image_to_string(
        Image.open('tmp/ocr_actor.jpg'),
        lang="eng",
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    ) 
    print(txt)


if __name__ == "__main__":
    x1, y1, x2, y2 = get_pos()
    start_time = time()
    while True:
        if time() - start_time > 10.0:
            screen_shot(x1, y1, x2, y2)
            ocr_actors()
            start_time = time()