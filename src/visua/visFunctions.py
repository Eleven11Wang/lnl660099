import matplotlib.pyplot as plt

import time
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy import stats
import pandas as pd
import matplotlib.patches as mpatches
import random

def stemPlot_and_fftPlot(stem_dict,fft_ls_dict,idx_ls=[],save_name= ""):
    assert len(stem_dict) == len(fft_ls_dict)
    if not idx_ls:
        idx_ls=random.sample(range(1,len(stem_dict)),min(100,len(stem_dict))-1)
    a = 100  # number of rows
    b = 2  # number of columns
    c = 1  # initialize plot counter

    fig = plt.figure(figsize=(100, 10))

    for i in range(len(idx_ls)):
        plt.subplot(a, b, c)
        markerline, stemlines, baseline = plt.stem(stem_dict[idx_ls[i]], markerfmt=" ", use_line_collection=True)
        plt.setp(stemlines, linestyle="-", color="grey", linewidth=0.1)
        stemlines.set_color("gray")
        stemlines.set_linewidth(1)
        baseline.set_color('none')
        c = c + 1

        plt.subplot(a, b, c)
        plt.plot(fft_ls_dict[idx_ls[i]])
        c = c + 1

    plt.show()



def stemPlot(lx,name=None):
    planes = 30000
    data=[0]*planes
    for x in lx:
        data[x-1] = 1

    f, ax = plt.subplots(figsize=(20, 1))
    markerline, stemlines, baseline = plt.stem(data, markerfmt=" ", use_line_collection=True)
    plt.setp(stemlines, linestyle="-", color="grey", linewidth=0.1)
    stemlines.set_color("gray")
    stemlines.set_linewidth(1)
    baseline.set_color('none')
    plt.tight_layout()



def make_box(datals, namels,title,i,lim=[]):
    t, p = stats.ttest_ind(datals[0], datals[1])
    dataLs = []
    nameLs = []
    labels = []
    fig, axes = plt.subplots(1, 2, figsize=(18, 10))

    for idx, data in enumerate(datals):
        for l in data:
            dataLs.append(l)
            nameLs.append(namels[idx])
    d = {'data': dataLs, 'name': nameLs}
    df = pd.DataFrame(data=d)

    ax = sns.violinplot(ax = axes[0],x='name', y='data', data=df)  # ,inner="quartile"
    if lim:
        ax.set_ylim(lim)
    #ax.set_ylabel("on state duration")
    labels.append((mpatches.Patch(color="blue"), "mean Atto: {:.3f}".format(sum(datals[0]/len(datals[0])))))
    labels.append((mpatches.Patch(color="orange"), "mean AF: {:.3f}".format(sum(datals[1]/len(datals[1])))))
    # Add jitter with the swarmplot function.
    # ax = sns.swarmplot(x='data', y='name', data=df, color="grey")
    plt.legend(*zip(*labels))
    #plt.tight_layout()
    plt.title(title+"    t : {:.2f}, p: {:.2f}".format(t,p))

    axes[1].hist(datals[0],bins = 50,alpha = 0.7)
    axes[1].hist(datals[1], bins= 50, alpha=0.7)

    if lim:
        axes[1].set_xlim(lim)
    axes[1].set_yscale('log')
    #plt.show()
    plt.savefig(title+str(i)+".png")
    plt.close()


