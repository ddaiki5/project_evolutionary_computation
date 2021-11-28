import numpy as np
import itertools
import random
import re
from ocr_score import Ocr

def crossover(chromo, parents, alpha=0.5) -> np.ndarray:
    '''
    交叉を行う

    Parameters
    ----------
    chromo : np.ndarray
        染色体配列を含む遺伝子の二次元配列
    parents : np.ndarray 
        親の染色体配列を含む遺伝子の二次元配列 
    alpha : float, default 0.5
        二点交叉の割合　残りは一様交叉を行う
    
    Retuens
    ----------
    children_chromo : np.ndarray
        子の染色体配列を含む遺伝子の二次元配列
    '''
    p_size, choromo_length = chromo.shape
    children_chromo = list()
    # 二点交叉
    counter = 0
    end = int(p_size*alpha)
    while counter<end:
        sp1 = random.randint(0, choromo_length-1)
        sp2 = random.randint(sp1, choromo_length)
        for pair in itertools.combinations(parents, 2):
            c1 = pair[0].copy()
            c2 = pair[1].copy()
            c1[sp1:sp2], c2[sp1:sp2] = pair[1][sp1:sp2], pair[0][sp1:sp2]
            children_chromo.append(c1)
            counter += 1
            if counter >= end:
                break
            children_chromo.append(c2)
            counter += 1

    # 一様交叉   
    end = p_size
    while counter<end:
        mask = np.random.randint(0, 2, (choromo_length))
        for pair in itertools.combinations(parents, 2):
            c1 = pair[0].copy()
            c2 = pair[1].copy()
            c2[mask==1] = pair[0][mask==1]
            c1[mask==1] = pair[1][mask==1]
            children_chromo.append(c1)
            counter+=1
            if counter >= end:
                break
            children_chromo.append(c2)
            counter += 1   
    return np.array(children_chromo)

def evaluate(ocr) -> float:
    '''
    評価を行う

    Parameters
    ----------
    ocr : Ocr instance
        画像文字認識を行う
    '''

    txt = ocr.ocr_actors()

    # 正規表現で符号あり0省略なしでマッチする
    m = re.search(r'[+-]?\d+(?:\.\d+)?', txt)
    result = m.group()
    return float(result)


def save_genetic_param(chromo, fitness, generation) -> None:
    np.savez("param/chromo_gen{}.npz".format(generation), c=chromo, f=fitness)

def load_genetic_param(generation) -> np.ndarray:
    npzfile = np.load("param/chromo_gen{}.npz".format(generation))
    return npzfile["c"], npzfile["f"]
    

if __name__ == "__main__":
    chromo = np.random.randint(0, 21, (100, 100))
    fitness = np.zeros(100)
    parents = chromo[0:5]
    new_chromo = crossover(chromo, parents, alpha=0.5)
    save_genetic_param(chromo, fitness, 1)
    print(load_genetic_param(1))

