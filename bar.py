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
    
    # Sample data : Counts for each group
    #          count
    # Group 1     12
    # Group 2      8
    # Group 3     19
    # Group 4     30
    df = pd.DataFrame({'count':[12, 8 ,19, 30]}, index = ['Group '+str(x) for x in range(1,5,1)])
    
    # Bar
    ax = df.plot.barh(align='center', color='#0080FF', legend = False)
    
    plt.show()