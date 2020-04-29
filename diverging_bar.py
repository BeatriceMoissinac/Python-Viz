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


# Colors
color = ['#ffffff','#ffeda0','#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c','lightgrey', "grey"]



def sorting(df, answers):
    
    df['positive'] = df[answers[-2:]].sum(axis=1)
    df = df.sort_values('positive', ascending=True).drop(columns=['positive'], axis=1)
    df = df.reindex(answers, axis=1)
    return df


# Define the tick of the x-axis depending on the number of answers
def stepSize(longest):
    if longest > 100:
        step = 50
    elif longest > 50:
        step = 20
    else:
        step = 5
        
    return step



if __name__ == "__main__": 
    
    answers = ['Never', 'Rarely', 'Sometimes', 'Often','Always']
    
    # Sample data
    #         Always  Never  Often  Rarely  Sometimes
    # Q1      13      1     10       4          7
    # Q2      14      2     11       5          8
    # Q3       2      3     12       6          9
    df = pd.DataFrame({'Never':[1,2,3], 'Rarely':[4,5,6], 'Sometimes':[7,8,9], 
                       'Often':[10,11,12], 'Always':[13,4,2]},
                      index = ['Q1','Q2','Q3'])
    
    df = sorting(df, answers)
    
    # Center the responses over the neutral answer where index=2 here is the neutral value

    middles = df[answers[:2]].sum(axis=1)+df[answers[2]]*0.5
    
    # Find the longest middle
    longest = int(middles.max())
    complete_longest = df.sum(axis=1).max() # largest number of responses for that question
    # Add the point where it will be centered
    df.insert(0, '', (middles - longest).abs())
    ax = df.plot.barh(stacked=True, color=color, edgecolor='none', legend=False, 
                      label=[None]+answers)
    ax.yaxis.tick_right()
  
 
    # Add legend  
    plt.subplots_adjust(bottom=0.10)  
    plt.legend(loc="lower center", ncol=3, fontsize=14, bbox_to_anchor=(0.5,-0.5),borderaxespad=0.) 
 
    # Add vertical line   
    z = plt.axvline(longest, linestyle='--', color='black', alpha=.5)
    z.set_zorder(-1)
      
    # X axis magic
    xmin = int(-(complete_longest-longest))
    xmax = int(complete_longest+longest)
    plt.xlim(xmin,xmax)
      
    # Get size step for xticks
    step = stepSize(complete_longest)
          
    # Magic x-axis
    xlabels1 = list(range(longest, xmax, step))
    xlabels = xlabels1[1:][::-1] + xlabels1
    xlabels = [str(int(x-longest)) for x in xlabels]
    xvalues = [longest-x*step for x in range(1,len(xlabels1),1)] + xlabels1
    xvalues = sorted(xvalues)
    
    plt.xticks(xvalues, xlabels)
    plt.xlabel('Number of Response', fontsize = 16)
    plt.tight_layout() # That's just so the .show() works correctly
    plt.show()
    