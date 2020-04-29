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
color   = ['#b10026','#e31a1c','#fc4e2a','#fd8d3c','#feb24c','#fed976','#ffeda0']


 # The label inside the slice is displayed only if it represents more than 5% of the total
def make_autopct(total):
    def my_autopct(pct):
        val = int(round(pct*total/100.0))
        return '{p:.2f}%\n({v:d})'.format(p=pct,v=val) if pct > 8 else ''
    return my_autopct




# Cosmetic function
def fontsizeLabels(fontsize=16):
    # Font size label "Profile"
    for text in texts:
        text.set_visible(True)
        text.set_fontsize(fontsize)
        
     # Color of label inside slice   
    autotexts[0].set_color('white') # Make first label white
    autotexts[1].set_color('white') # Make second label white
    for autotext in autotexts:
        autotext.set_fontsize(fontsize)



if __name__ == "__main__": 
    
    # Sample data : Counts for each group
    #          count
    # Group 1     12
    # Group 2      8
    # Group 3     19
    # Group 4     30
    df = pd.DataFrame({'count':[12, 8 ,19, 30]}, index = ['Group '+str(x) for x in range(1,5,1)])
    total = df['count'].sum()
    
    patches, texts, autotexts = plt.pie(df['count'], 
            colors  = color,    # Colors 
            labels  = df.index, # Labels on each patch
            startangle=90,      # First slice starts straight at "midnight"
            counterclock= False,# Categories are ordered clockwise
            autopct = make_autopct(total)) # Labels inside slices
    
    # set fontsize 
    fontsizeLabels(fontsize=16) 
    
    #plt.savefig("pathToSomewhere/myFile.png", bbox_inches='tight')
    plt.show()
    
    
    