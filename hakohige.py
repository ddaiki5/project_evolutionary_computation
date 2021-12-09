import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib       # グラフに日本語が使える
from genetic_utils import load_genetic_param
import pandas as pd
import numpy as np

plt.style.use("ggplot")
plt.figure(figsize=(10,6))
sns.set_palette("Set2")
_, fitness1 = load_genetic_param(1)
print(fitness1)
_, fitness4 = load_genetic_param(20)
_, fitness2 = load_genetic_param(50)
_, fitness3 = load_genetic_param(100)
#f = [[1, fitness1], [50, fitness2], [100, fitness3]]

fig, ax = plt.subplots()
ax.set_xticklabels(['1', '10', '30', '50', '100'])
ax.boxplot((fitness1, fitness4, fitness2, fitness3), whis="range")



#plt.title("QWOP最適化",fontsize=20)   # タイトルを指定する、文字の大きさを指定
plt.ylabel("走行距離")         # ｙ軸のラベルを指定、文字の大きさを指定
plt.xlabel("世代")           # ｘ軸のラベルを指定、文字の大きさを指定

plt.show()