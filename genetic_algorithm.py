# 新谷担当
import numpy as np
import time
from keytest_ import KeyOutputList
from genetic_utils import evaluate, crossover, save_genetic_param, load_genetic_param
from genetic_select import roulette_select, mutate
from ocr_score import Ocr
import pyautogui

def run_generation(chromo, generation) -> np.ndarray:
    '''
    1世代分の学習を行う

    Parameters
    ----------
    chromo :  np.ndarray
        染色体配列を含む遺伝子の二次元配列
    '''
    fitness = np.zeros(100) #適応度初期化
    for i in range(len(chromo)):
        print("{}世代{}個目".format(generation, i))
        KOLtest = KeyOutputList()
        KOLtest.read_gene(chromo[i])
        KOLtest.print_keylist()
        KOLtest.output(10.0) # key出力
        fitness[i] = evaluate(ocr) #適応度を返す

        # 入力の初期化
        pyautogui.press('r')
        pyautogui.press('q')
        pyautogui.press('w')
        pyautogui.press('o')
        pyautogui.press('p')
        pyautogui.press('r')
        time.sleep(1)
    save_genetic_param(chromo, fitness, generation) # パラメータ保存
    print("fitness 最大:{} 平均{}".format(np.amax(fitness), np.average(fitness)))
    parents = roulette_select(chromo, fitness) #選択
    new_chromo = crossover(chromo, parents, alpha=0.5) #交叉
    chromo = mutate(new_chromo) #突然変異
    return chromo
    
def load_generation(gen) -> np.ndarray:
    '''
    指定した世代の保存したパラメータを呼び出し、選択、交叉、突然変異を行う
    '''
    chromo, fitness = load_genetic_param(gen)
    parents = roulette_select(chromo, fitness)
    new_chromo = crossover(chromo, parents, alpha=0.5)
    chromo = mutate(new_chromo)
    return chromo

def run(gen) -> None:
    '''
    指定した世代を学習を行わずに実行する
    '''
    chromo, fitness = load_genetic_param(gen)
    print("-------------------")
    print("{}世代　Start".format(gen))
    chromo = run_generation(chromo, gen)
    print("-------------------")

def train() -> None:
    '''
    遺伝的アルゴリズムの学習を行う
    '''

    #染色体の初期化
    chromo = np.random.randint(0, 21, (100, 100))
    max_gen = 100
    # 1から100世代まで学習する
    for i in range(1, max_gen+1): 
        print("-------------------")
        print("{}世代　Start".format(i))
        chromo = run_generation(chromo, i)
        print("-------------------")

if __name__ == '__main__':
    # メイン関数
    ocr = Ocr() # OCRの行う
    train() #学習をする
    

