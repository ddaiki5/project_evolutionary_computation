import numpy as np
import random

def roulette_select(chromo, fitness):
    '''
    ルーレット選択

    Parameters
    ----------
    chromo : np.ndarray
        染色体配列を含む遺伝子の二次元配列
    fitness : np.ndarray
        進んだ距離

    Retuens
    ----------
    parents : np.ndarray
        親の染色体配列を含む遺伝子の二次元配列
    '''
    fit_sort = np.sort(fitness)#昇順にソート
    fit_argsort = np.argsort(fitness)#昇順にソートした際のインデックス
    fit_sort = np.where(fit_sort<0,0,fit_sort)#0未満を0に置換
    parents = list()

    for p in range(5):#ルーレット選択を5回
        fit_prob = fit_sort/np.sum(fit_sort)
        for i in range(fit_prob.size-1):#確率の累積和をとる
            fit_prob[i+1] += fit_prob[i]
        random.seed()
        r = random.random()
        select = np.count_nonzero(fit_prob < r)
        parents.append(chromo[fit_argsort[select]])
        fit_sort = np.delete(fit_sort,select)
        fit_argsort = np.delete(fit_argsort,select)

    return np.array(parents)

def mutate(chromo):
    '''
    突然変異

    Parameters
    ----------
    chromo : np.ndarray
        染色体配列を含む遺伝子の二次元配列

    Retuens
    ----------
    mutated_parents : np.ndarray
        突然変異済みの染色体配列を含む遺伝子の二次元配列
    '''
    random.seed()
    p_size, chromo_length = chromo.shape
    mutated_chromo = list()
    for i in range(p_size):
        if random.random()<=0.0005:#0.05%で完全ランダム
            mutated_chromo.append(np.random.randint(0, 21, chromo_length))
            continue
        new_chromo = list()
        for j in range(chromo_length):
            if random.random()<=0.005:#0.5%で遺伝子変異
                new_chromo.append(random.randint(0,20))
            else:
                new_chromo.append(chromo[i][j])
        mutated_chromo.append(new_chromo)

    return np.array(mutated_chromo)


if __name__ == "__main__":
    chromo = np.random.randint(0, 21, (100, 100))
    fitness = np.random.uniform(0.0, 10.0, 100)
    print(chromo)
    print(fitness)
    print(roulette_select(chromo, fitness))
    print(mutate(chromo))
