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

        # 3秒待ってからカーソル位置の座標を取得
        print("右下隅の座標を取得します")
        sleep(3)
        x2, y2 = pyautogui.position()
        print(str(x2) + "," + str(y2))

        # # PyAutoGuiのregionの仕様のため、相対座標を求める
        x2 -= x1
        y2 -= y1

        return (x1, y1, x2, y2)

    def _screen_shot(self) -> None:
        '''
        pyautoguiを使用して指定した場所のスクリーンショットを取得して保存する
        '''
        sc = pyautogui.screenshot(region=self.pos) # get_pos関数で取得した座標を使用

        # 上のスコア部分切り出し
        sc.crop((200*self.pos[2]/640, 15*self.pos[3]/400, 415*self.pos[2]/640, 55*self.pos[3]/400)).save(self._image_up_path)

        # 中央のスコア部分切り出し
        sc.crop((250*self.pos[2]/640, 185*self.pos[3]/400, 385*self.pos[2]/640, 215*self.pos[3]/400)).save(self._image_mid_path)

    def _exec_ocr(self, index) -> str:
        '''
        保存した画像から文字認識を行う

        Retuens
        ----------
        txt : str
            認識した文字を文字列として返す
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

        Retuens
        ----------
        result : float
            正規表現でマッチしたスコアの小数部分を返す
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
            # 中央部と上部のスコアが離れすぎているときを除外
            if abs(float(result1)-float(result)) < 2.0:
                return float(result1)
            else:
                return float(result)

if __name__ == "__main__":
    # テスト用
    ocr = Ocr()
    print(ocr.ocr_actors())
