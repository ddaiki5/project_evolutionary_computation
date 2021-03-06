import numpy as np
import itertools
import random
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
    p_size, chromo_length = chromo.shape
    children_chromo = list()
    children_chromo.extend(parents) #親は次の世代に入る
    counter = 5

    # 二点交叉
    end = int(p_size*alpha)
    while counter<end:
        # ランダムな2点選択
        sp1 = random.randint(0, chromo_length-1)
        sp2 = random.randint(sp1, chromo_length)
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
        # ランダムなマスクを作成
        mask = np.random.randint(0, 2, (chromo_length))
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
    return np.array(children_chromo[:100])

def evaluate(ocr) -> float:
    '''
    評価を行う

    Parameters
    ----------
    ocr : Ocr instance
        画像文字認識を行う
    
    Retuens
    ----------
    score : float
        到達した距離
    '''

    score = ocr.ocr_actors()
    print("Score: ", score)
    return score


def save_genetic_param(chromo, fitness, generation) -> None:
    '''
    染色体と適応度のパラメータを保存
    '''
    np.savez("param/chromo_gen_re{}.npz".format(generation), c=chromo, f=fitness)

def load_genetic_param(generation) -> np.ndarray:
    '''
    指定した世代の染色体と適応度のパラメータを取得
    '''
    npzfile = np.load("param/chromo_gen_re{}.npz".format(generation))
    return npzfile["c"], npzfile["f"]
    

if __name__ == "__main__":
    # テスト用
    _, fitness = load_genetic_param(27)
    print(fitness)
