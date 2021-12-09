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
    Parameters
    ----------
    filename : str
        txtファイルのファイル名

    filenameで指定したtxtファイルからキー出力のパターンを読み込み、keylistに代入する
    txtファイルの書き方はtest.txt参照

・read_gene(self, gene)
    Parameters
    ----------
    gene : np.ndarray
        染色体配列(1次元配列)

    geneで指定した染色体の遺伝子(0～20の整数)を読み込み、キー出力のパターンに変換し、keylistに代入する

・print_keylist(self)
    keylistの中身を出力する

・output(self, t)
    キー出力をkeylistに従って行う
    t秒経過するか、keylistを全てキー出力し終えたら関数を終了する

キー出力パターンと数字の対応
0,1,2:noneの0.1,0.5,0.8
3,4,5:Qの0.1,0.5,0.8
6,7,8:Wの...
9,10,11:O
12,13,14:P
15,16,17:Q+P
18,19,20:W+O
"""

SECLIST = (0.1, 0.5, 0.8)#秒数のリスト、read_geneで使用
WORDLIST = (['none'], ['q'], ['w'], ['o'], ['p'], ['q','p'], ['w','o'])#キーのリスト、read_geneで使用

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

    def read_gene(self, gene):
        for genome in gene:
            newkeylist = list()
            newkeylist.extend(WORDLIST[genome//3])#数字の剰余と商からキー出力を求める
            newkeylist.append(SECLIST[genome%3])
            self.keylist.append(newkeylist)

    def print_keylist(self):
        print(self.keylist)

    def output(self, t):
        t1 = time.time()
        for keydata in self.keylist:
            sec = keydata.pop(-1)
            for key in keydata:
                pyautogui.keyDown(key)#キーを押す
            time.sleep(sec)
            for key in keydata:
                pyautogui.keyUp(key)#キーを離す
            t2 = time.time()
            if(t2-t1>t):#指定時間を越えたら終了
                break

#以下テスト用
# time.sleep(2)
# KOLtest = KeyOutputList()
# chromo = np.random.randint(0, 21, (5, 10))
# KOLtest.read_gene(chromo[0])
# KOLtest.print_keylist()
# KOLtest.output()
