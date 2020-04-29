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


markers = ('+','*', 'o', 'v', 'x', 's', '.') 
color = ['#ffeda0','#fed976','#feb24c','#fd8d3c', '#fc4e2a','#e31a1c','#b10026',]
linestyles = ['-', '-.', '--', ':']

if __name__ == "__main__": 
    
    df = pd.DataFrame({'line0':[1,2,3,4], 'line1':[2,4,6,8], 'line2':[3,6,9,12], 'line3':[4,8,12,16]})
    print(list(df.index))
    nx = 2 # Number of plots on x axis
    ny = 2 # Number of plots on y axis
    
    # Subplot handler
    f, axArr = plt.subplots(nx, ny, sharex='col', sharey='row')

    col = list(df.columns)  # List of column to iterate through
    idxcol = 0              # Index of column list

    for i in range(0,nx,1):
        for j in range(0,ny,1):

            # Subplot i,j
            axArr[i,j].plot(df.index,
                         df[col[idxcol]],         # The data
                         marker    = markers[idxcol],    # Marker of point
                         linewidth = 2.0,           # Can't you read?
                         color     = color[idxcol],      # Color
                         alpha     = 1              # Visbility
                        )
            
            # Add Error bar shade
            y1 = np.array(df[col[idxcol]])-np.array(df[col[idxcol]])
            y2 = np.array(df[col[idxcol]])+np.array(df[col[idxcol]])
            axArr[i, j].fill_between(
                x          = df.index,
                y1         = y1,                # Below average
                y2         = y2,                # Above average
                color      = color[idxcol],          # Color    
                alpha      = 0.3,               # Transparency
                linewidth  = 2,                 # Border thickness
                linestyle  = linestyles[idxcol%4])   # Style of boarder
            
            # Cosmetics
            axArr[i, j].set_title(col[idxcol])  
            
            # Increment col index
            idxcol += 1
            
    plt.show()