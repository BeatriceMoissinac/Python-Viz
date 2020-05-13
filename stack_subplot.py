"""
Demonstration code for matplotlib figure generation
Author: Beatrice Moissinac
"""


import csv 
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import numpy as np
import os
import pandas as pd
import sys


if __name__ == "__main__": 
  
  import csv 
from io import StringIO, BytesIO
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import numpy as np
from os import listdir
import pandas as pd
import sys



def stacked_area(df, source, device):
     
    col = 'Profile_' + device
    maxPf = int(df[df[col] != 'No Profile'][col].max())
    
    x = ['Freshman', 'Sophomore', 'Junior', 'Senior']
    

    f, (ax1, ax2, ax3) = plt.subplots(1,3, sharey=True, figsize=(20, 20))
    ct1 = stackHelper(df, "A", col, x, maxPf)
    ct2 = stackHelper(df, "B", col, x, maxPf)
    ct3 = stackHelper(df, "C", col, x, maxPf)
    
    plt.rcParams.update({'font.size': 50, 'ytick.labelsize':50, 'xtick.labelsize':50})
    plt.tight_layout()


    # Y ticks in percentage
    plt.yticks(np.arange(0, 1.1, 0.2),fontsize=50,)
    vals = ax1.get_yticks()
    ax1.set_yticklabels(['{:.1f}%'.format(v*100) for v in vals],fontsize=65,)
    
    ax1 = stacker(ax1, ct1, x, maxPf)
    ax1.set_title('CS Students')
    ax2 = stacker(ax2, ct2, x, maxPf)
    ax2.set_title("CoE Students")
    ax3 = stacker(ax3, ct3, x, maxPf)
    ax3.set_title("All Students")
    #plt.show()
    term, pop, cohort = file.split("_") 
    plt.savefig('/Users/moissinb/workspace/IS-Pipeline/data/outputs/plots/' + source + '/' + term + '/' + pop + '/' + cohort +
                 '/' + device + '/' + source + '_' + file + '_' + device +'_LapReqVSYearCSCoeAll.png', bbox_inches='tight')


def stacker(ax, data, x, maxPf):
    color = ['#ffeda0','#fed976','#feb24c','#fd8d3c', '#fc4e2a','#e31a1c','#b10026',]
    labels = ['No Profile'] + list(reversed(range(1,maxPf+1)))
    
    ax.stackplot(np.arange(len(x)), data, labels=labels, colors = color)
    ax.set_xticks(np.arange(len(x)))
    ax.set_xticklabels(x, rotation = 45, ha="right",fontsize=50)
    
    # Add labels within shaded area
    temp = data[0][1]
    pct = temp / 2
    ax.text(0.5, pct, labels[0],fontsize=50)
    for v in range(1,maxPf+1):
        pct = temp + data[v][1]/3
        temp += data[v][1]
        if data[v][1] > 0.08:
            if v in range(1,maxPf+1)[-2:]:
                ax.text(0.5, pct, 'Profile '+str(labels[v]),  color = 'white',fontsize=50)
            else :
                ax.text(0.5, pct, 'Profile '+str(labels[v]),fontsize=50)

 
    return ax






def stackHelper(df, Req, col, x, maxPf):
    y = []
    y1= []
    for year in x:
        filter = df[(df.LapReq == Req) & (df[col] == 'No Profile') & (df['Class Standing Desc'] == year)]
        try:
            val = filter.iloc[0]['Percentage'] 
        except IndexError:
            val = 0
        y1.append(val)
    y.append(y1) 
    for i in reversed(range(1, maxPf + 1)):
        y1 = []
        # i^th profile
        for year in x:
            filter = df[(df.LapReq == Req) & (df[col] == str(i)) & (df['Class Standing Desc'] == year)]
            try:
                val = filter.iloc[0]['Percentage'] 
            except IndexError:
                val = 0
            y1.append(val)          
        y.append(y1)  
    return y



def readCSV(file, device):
    onlyfiles = ["/Users/moissinb/workspace/Aruba2/data/outputs/Task9b/" + file + "/" + device + "/" + f 
                for f in listdir("/Users/moissinb/workspace/Aruba2/data/outputs/Task9b/" + file + "/" + device + "/") if str(f)[-4:] == ".csv"]
    df = pd.read_csv(onlyfiles[0])
    return df
    
if __name__ == "__main__": 
    file = sys.argv[1]
    device = sys.argv[2]
    source = sys.argv[3]
    
#     file = "F17_udg_over18"
#     source = "Labstat"
#     device = "Desktop"
    
    df = readCSV(file, device)
    print(df)
    plt = stacked_area(df, source, device)
