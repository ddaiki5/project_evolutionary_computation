# 遺伝的アルゴリズムを用いたQWOPの最適化

##概要

Webブラウザ上のゲームQWOPを遺伝的アルゴリズムでキー入力の最適化しハイスコアを目指す

## 遺伝的アルゴリズム

生物の進化を模した解探索のアルゴリズム

## QWOP

Q、W、O、Pだけで移動するゲーム

http://www.foddy.net/Athletics.html

## GAのパラメータ

個体数: 100

個体表現: Q, W, O, P, Q+P, W+O, none(無入力)の7種類とキーを押した時間0.1、0.5、0.8の三種類の組み合わせ21種類

親の選択方法: ルーレット選択

交叉方法: 二点交叉と一様交叉を混合

解の評価方法: 制限時間内に進めた距離の三乗

交叉率: 0.95(親5個体、二点交叉45個体、一様交叉50個体)

突然変異率: 0.8%
