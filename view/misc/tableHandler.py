import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import table

class tableHandler:
    data = {}
    def setFont():
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
        plt.rcParams['axes.unicode_minus'] = False
    def readAll():
        with open('freq.json', encoding="UTF-8") as ifs:
            tableHandler.data = json.loads(ifs.read())
    def articleHandler():
        fileID = 0
        fileNum = len(tableHandler.data.items())
        for articleName, wordlist in tableHandler.data.items():
            print(f"Processing file {articleName}\t({fileID}/{fileNum})")
            fileID += 1
            
            xs = [word for word, cnt in wordlist]
            ys = [int(cnt) for word, cnt in wordlist]
            x_pos = [i for i, _ in enumerate(xs)]
            
            fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
            plt.bar(xs, ys, color='green')
            ax.set_xlabel("詞彙", fontsize=25)
            ax.set_ylabel("數量", fontsize=25)
            ax.set_title(articleName, fontsize=50)
            ax.set_xticks(x_pos)
            # plt.show()
            fig.set_size_inches(24, 13.5)
            fig.savefig(f'./img/{articleName}.png')   # save the figure to file
            plt.close(fig)    # close the figure window
    def driver():
        tableHandler.setFont()
        tableHandler.readAll()
        tableHandler.articleHandler()
tableHandler.driver()