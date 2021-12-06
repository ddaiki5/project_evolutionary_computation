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
import re

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

def get_pos() -> tuple:
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

    return (x1, y1, 640, 400)

def screen_shot(x1, y1, x2, y2) -> None:
    '''docstring
    pyautoguiを使用して指定した場所のスクリーンショットを取得して保存する
    '''
    sc = pyautogui.screenshot(region=(x1, y1, x2, y2))  # get_pos関数で取得した座標を使用
    sc.crop((200, 15, 415, 55)).save('tmp/ocr_actor1.jpg')
    sc.crop((250, 185, 385, 215)).save('tmp/ocr_actor2.jpg')

    

def ocr_actors() -> None:
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

def ocr_score_finish():
    sc = pyautogui.screenshot(region=(611, 359, 195, 40))  # get_pos関数で取得した座標を使用
    sc.save('tmp/ocr_actor1.jpg')
    txt = tool.image_to_string(
    Image.open('tmp/ocr_actor1.jpg'),
        lang="eng",
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        )
    m = re.search(r'[+-]?\d+(?:\.\d+)?', txt)
    result = m.group()
    #print(result)


    txt = tool.image_to_string(
        Image.open('tmp/ocr_actor.jpg'),
        lang="eng",
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    ) 
    #print(txt)
    m = re.search(r'[+-]?\d+(?:\.\d+)?', txt)
    try:
        result1 = m.group()
    except Exception as e:
        print("except", result)
        return float(result)
    else:
        print(result, result1)
        if abs(float(result1)-float(result)) < 1.5:
            return float(result1)
        else:
            return float(result)


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class Ocr:
    def __init__(self):
        self.pos = self.get_pos()
        self._image_up_path = 'tmp/ocr_actor1.jpg'
        self._image_mid_path = 'tmp/ocr_actor2.jpg'


    @classmethod
    def get_pos(cls) -> tuple:
        '''
        pyautoguiを使用してスクリーンショットのための座標の取得\n
        ３秒ごとに左上と右下の座標を取得する
        '''

        # 3秒待ってからカーソル位置の座標を取得
        print("左上隅の座標を取得します")
        sleep(3)
        x1, y1 = pyautogui.position()
        print(str(x1) + "," + str(y1))

        # # 3秒待ってからカーソル位置の座標を取得
        # print("右下隅の座標を取得します")
        # sleep(3)
        # x2, y2 = pyautogui.position()
        # print(str(x2) + "," + str(y2))

        # # PyAutoGuiのregionの仕様のため、相対座標を求める
        # x2 -= x1
        # y2 -= y1

        return (x1, y1, 640, 400)

    def _screen_shot(self) -> None:
        '''
        pyautoguiを使用して指定した場所のスクリーンショットを取得して保存する
        '''
        sc = pyautogui.screenshot(region=self.pos)  # get_pos関数で取得した座標を使用

        # 上のスコア部分切り出し
        sc.crop((200, 15, 415, 55)).save(self._image_up_path)

        # 中央のスコア部分切り出し
        sc.crop((250, 185, 385, 215)).save(self._image_mid_path)

    def _exec_ocr(self, index) -> str:
        '''
        保存した画像から文字認識を行う
        現状認識した文字をすべて表示している
        '''
        txt = tool.image_to_string(
            Image.open('tmp/ocr_actor{}.jpg'.format(index)),
            lang="eng",
            builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        ) 
        return txt
    
    def ocr_actors(self) -> float:
        '''
        取得した文字列を正規表現にかけて少数部分だけ取り出す\n
        中央部にスコアが表示されているときは中央スコア、中央部にスコアが表示されていないときは上部のスコアを用いる
        '''
        # 上部スコア取得
        self._screen_shot()
        txt = self._exec_ocr(1)
        # 正規表現で符号あり0省略なしでマッチする
        m = re.search(r'[+-]?\d+(?:\.\d+)?', txt) # 
        # エラー時は最大3回実行
        for _ in range(3):
            try:
                result = m.group()
            except Exception as e:
                self._screen_shot()
                txt = self._exec_ocr(1)
                m = re.search(r'[+-]?\d+(?:\.\d+)?', txt)
            else:
                break
        else:
            print("Error: ocr image_up failed", file = sys.stderr)

        # 中央のスコア取得
        txt = self._exec_ocr(2)
        # 正規表現で符号あり0省略なしでマッチする
        m = re.search(r'[+-]?\d+(?:\.\d+)?', txt)
        try:
            result1 = m.group()
        except Exception as e: #中央部にスコアが表示されていないとき
            return float(result)
        else:
            # 中央部と上部のスコアが離れすぎているとき
            if abs(float(result1)-float(result)) < 1.5:
                return float(result1)
            else:
                return float(result)



if __name__ == "__main__":
    # x1, y1, x2, y2 = get_pos()
    # print(x1, y1, x2, y2)
    # screen_shot(x1, y1, x2, y2)
    ocr = Ocr()
    print(ocr.ocr_actors())
    
    # start_time = time()
    # while True:
    #     if time() - start_time > 5.0:
    #         screen_shot(639, 529, 153, 25)
    #         print("result", ocr_score_finish())
    #         start_time = time()