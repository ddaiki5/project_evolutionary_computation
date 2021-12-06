import random
import numpy as np
import time
from keytest_ import KeyOutputList
from genetic_utils import evaluate, crossover, save_genetic_param, load_genetic_param
from genetic_select import roulette_select, mutate
from ocr_score import Ocr
import pyautogui


def run_generation(chromo, generation):
    fitness = np.zeros(100)
    for i in range(len(chromo)):
        time_sta = time.time()
        print("{}世代{}個目".format(generation, i))
        KOLtest = KeyOutputList()
        KOLtest.read_gene(chromo[i])
        KOLtest.print_keylist()
        KOLtest.output(5.0)
        fitness[i] = evaluate(ocr)
        pyautogui.press('r')
        pyautogui.press('q')
        pyautogui.press('w')
        pyautogui.press('o')
        pyautogui.press('p')
        pyautogui.press('r')
        time.sleep(1)
    save_genetic_param(chromo, fitness, generation)
    print("fitness 最大:{} 平均{}".format(np.amax(fitness), np.average(fitness)))
    parents = roulette_select(chromo, fitness)
    new_chromo = crossover(chromo, parents, alpha=0.5)
    chromo = mutate(new_chromo)
    return chromo
    
def load_generation(gen):
    chromo, fitness = load_genetic_param(gen)
    parents = roulette_select(chromo, fitness)
    new_chromo = crossover(chromo, parents, alpha=0.5)
    chromo = mutate(new_chromo)
    return chromo


def run(gen):
    chromo, fitness = load_genetic_param(gen)
    #ocr = Ocr()
    #max_gen = 100 
    print("-------------------")
    print("{}世代　Start".format(gen))
    chromo = run_generation(chromo, gen)
    print("-------------------")

def train():
    chromo = load_generation(53)
    #染色体　遺伝子100×一世代数100
    #chromo = np.random.randint(0, 21, (100, 100))
    #OCR
    #ocr = Ocr()
    max_gen = 100
    for i in range(54, max_gen): 
        print("-------------------")
        print("{}世代　Start".format(i))
        chromo = run_generation(chromo, i)
        print("-------------------")


if __name__ == '__main__':
    ocr = Ocr()
    train()
    

