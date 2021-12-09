import pyautogui
import time
import numpy as np
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


0,1,2:noneの0.1,0.5,0.8
3,4,5:Qの0.1,0.5,0.8
6,7,8:Wの...
9,10,11:O
12,13,14:P
15,16,17:Q+P
18,19,20:W+O
"""

SECLIST = (0.100, 0.500, 0.800)
WORDLIST = (['none'], ['q'], ['w'], ['o'], ['p'], ['q','p'], ['w','o'])

class KeyOutputList(object):
    def __init__(self):
        self.keylist = []
        self.over = False

    def read_keylist(self, filename):
        file = open(filename, 'r')
        text = file.readlines()
        i=0
        for sentence in text:
            self.keylist.append(sentence.split(','))
            self.keylist[-1][-1] = float(self.keylist[-1][-1])

    def read_gene(self, gene):
        for genome in gene:
            newkeylist = list()
            newkeylist.extend(WORDLIST[genome//3])
            newkeylist.append(SECLIST[genome%3])
            self.keylist.append(newkeylist)

    def print_keylist(self):
        print(self.keylist)

    def output(self, t, ocr):
        self.over = False
        t1 = time.time()
        for keydata in self.keylist:
            sec = keydata.pop(-1)
            for key in keydata:
                pyautogui.keyDown(key)
            time.sleep(sec)
            for key in keydata:
                pyautogui.keyUp(key)
            score, f = ocr.ocr_actors1()
            t2 = time.time()
            if(t2-t1>t or f):
                return t2-t1



# time.sleep(2)
# KOLtest = KeyOutputList()
# chromo = np.random.randint(0, 21, (5, 10))
# KOLtest.read_gene(chromo[0])
# KOLtest.print_keylist()
# KOLtest.output()
