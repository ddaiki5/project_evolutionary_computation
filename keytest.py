import pyautogui
import time
"""
KeyoutputList クラス
キーボード出力のためのクラス
インスタンス
・keylist
    ['出力するキー','出力するキー',...,出力する秒数]を要素とするリスト(多重リスト)

関数
・read_keylist(self,filename)
    filenameで指定したtxtファイルからキー出力のパターンを読み込み、keylistに代入する
    txtファイルの書き方はtest.txt参照

・print_keylist(self)
    keylistの中身を出力する

・output(self)
    キー出力をkeylistに従って行う
"""

class KeyOutputList(object):
    def __init__(self):
        self.keylist = []

    def read_keylist(self, filename):
        file = open(filename, 'r')
        text = file.readlines()
        i=0
        for sentence in text:
            self.keylist.append(sentence.split(','))
            self.keylist[-1][-1] = float(self.keylist[-1][-1])

    def print_keylist(self):
        print(self.keylist)

    def output(self):
        for keydata in self.keylist:
            sec = keydata.pop(-1)
            for key in keydata:
                pyautogui.keyDown(key)
            time.sleep(sec)
            for key in keydata:
                pyautogui.keyUp(key)

time.sleep(2)
KOLtest = KeyOutputList()
KOLtest.read_keylist('test.txt')
KOLtest.print_keylist()
KOLtest.output()
