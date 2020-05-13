"""
This program produces the stacked plot if the number of days users have brought theyr device, per week of a term
Usage:
python3 plot_task1.py <aws-profile> <cohort> <device> <source>
python3 plot_task1.py MoissinB Sp17_udg_all Laptop Labstat
"""

import boto3
import csv 
from io import StringIO, BytesIO
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import numpy as np
import os
import pandas as pd
import sys





# Connect to AWS S3 using AWS CLI configured profile
def connectToAWS(profile):
    boto3.setup_default_session(profile_name=profile)  # Set profile
    client = boto3.client('s3')  # Client S3
    return client



# Returns dataFrame of csv file
def readFileCSV(file, client, source):
    for key in client.list_objects(Bucket='osu-is', Prefix=source.lower()+'/analysis/' + file + '.csv/')['Contents']:
        if key['Key'].endswith('.csv'):
            obj = client.get_object(Bucket='osu-is', Key=key['Key'])
            df = pd.read_csv(BytesIO(obj['Body'].read()), encoding='utf8')
            return df
    
    
def stacked_plot(df, cumul, device, source):
    # print(df[(df.TypeOfDevice == device)])
    df = df[(df.TypeOfDevice == device)].dropna()  # Filter for TypeOfDevice
    maxWeek = int(df.Week.max()) 

    minWeek = int(df.Week.min())
    # Pivot table
    pivot = list(np.zeros((maxWeek + 1, 8)))  # list of np.array number of Day x Week
    pivot_table = [list(l) for l in pivot]  # Convert np.array to list 
    
    for index, row in df.iterrows():
        pivot_table[int(row['Week'])][row['NumberOfDays']] = int(row['count'])
     
    weeks = [w for w in range(0, maxWeek + 1)]     
    # weeks = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'] 
    for i in range(0, maxWeek + 1):
        pivot_table[i][0] = weeks[i]
    
    # Convert to DataFrame
    df2 = pd.DataFrame(pivot_table, columns=['Weeks', '1 day', '2 days', '3 days', '4 days', '5 days', '6 days', '7 days'])
    df2 = df2[(df2.T != 0).any()].reset_index(drop=True)  # Remove empty rows (Week 0 for any terms but Fall)
    print(df2)
    columns = ['1 day', '2 days', '3 days', '4 days', '5 days', '6 days', '7 days']
    
    plt.rcParams.update({'font.size': 22, 'figure.figsize':(200, 100), 'ytick.labelsize':28, 'xtick.labelsize':28})

    
    # Create the general blog and the "subplots" i.e. the bars
    f, ax1 = plt.subplots(1, figsize=(20, 15))
    
    # Set the bar width
    bar_width = 0.75
    
    # positions of the left bar-boundaries
    bar_l = df2['Weeks']
    
    patch_handles = []
    
    # Add 1Day
    patch_handles.append(ax1.bar(bar_l,
            # using the pre_score data
            df2['1 day'],
            # set the width
            width=bar_width,
            # with the label pre score
            label='1 Day',
            # with alpha 0.5
            alpha=1,
            # with color
            color='#ffffb2'))
    
    # Add 2Days
    patch_handles.append(ax1.bar(bar_l,
            df2['2 days'],
            width=bar_width,
            bottom=df2['1 day'],
            label='2 Days',
            alpha=1,
            color='#fed976'))
    
    
    patch_handles.append(ax1.bar(bar_l,
            df2['3 days'],
            width=bar_width,
            bottom=[i + j for i, j in zip(df2['1 day'], df2['2 days'])],
            label='3 Days',
            alpha=1,
            color='#feb24c'))
    
    
    patch_handles.append(ax1.bar(bar_l,
            df2['4 days'],
            width=bar_width,
            bottom=[i + j + k for i, j, k in zip(df2['1 day'], df2['2 days'], df2['3 days'])],
            label='4 Days',
            alpha=1,
            color='#fd8d3c'))
    
    patch_handles.append(ax1.bar(bar_l,
            df2['5 days'],
            width=bar_width,
            bottom=[i + j + k + l for i, j, k, l in zip(df2['1 day'], df2['2 days'], df2['3 days'], df2['4 days'])],
            label='5 Days',
            alpha=1,
            color='#fc4e2a'))
    
    patch_handles.append(ax1.bar(bar_l,
            df2['6 days'],
            width=bar_width,
            bottom=[i + j + k + l + m for i, j, k, l, m in zip(df2['1 day'], df2['2 days'], df2['3 days'], df2['4 days'], df2['5 days'])],
            label='6 Days',
            alpha=1,
            color='#e31a1c'))
    
    patch_handles.append(ax1.bar(bar_l,
            df2['7 days'],
            width=bar_width,
            bottom=[i + j + k + l + m + n for i, j, k, l, m, n in zip(df2['1 day'], df2['2 days'], df2['3 days'], df2['4 days'], df2['5 days'], df2['6 days'])],
            label='7 Days',
            alpha=1,
            color='#b10026'))
    
    
    total = list(df2.sum(1)) 
    for j in range(len(patch_handles)):
        for i, patch in enumerate(patch_handles[j].get_children()):
            bl = patch.get_xy()
            x = 0.5 * patch.get_width() + bl[0]
            y = 0.5 * patch.get_height() + bl[1]
            #print(bl[1] + patch.get_height())
            if j <= 4 and patch.get_height()/total[i] > 0.05:
                ax1.text(x, y, "%d" % df2.ix[i][j+1], ha='center')
            elif j > 4 and patch.get_height()/total[i] > 0.05:
                ax1.text(x, y, "%d" % df2.ix[i][j + 1], ha='center', color='white')
            else:
                pass
    #             elif device == "Phone":
    #                 ax1.text(x,y, "%d" % df2.ix[i+1][j+1], ha='center', color='white')
     

    plt.plot(bar_l, cumul, c='r', linewidth=4, marker='o', markersize=20, label="Cumulative")
  
       
    # ELEMENTS OF THE GRAPH

    # set the x ticks with names
    plt.xticks(bar_l, df2['Weeks'])
    
    # Set the label and legends
    ax1.set_ylabel("Number of Users", fontsize=40)
    ax1.set_xlabel("Weeks", fontsize=40)
    lgd = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10), ncol=4, fontsize=28)
    
    plt.savefig('data/outputs/plots/' + source + '/' + source + '_' + file + '_' + device + '_UsageInDaysPerWeek.png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    #plt.show()
    return
    
    
if __name__ == "__main__": 

    profile = sys.argv[1]  # AWS profile credential to use
    file = sys.argv[2]  # File to upload
    device = sys.argv[3]  # Laptop,Phone,Tablet,Desktop
    source = sys.argv[4]

#     profile = 'MoissinB'  # $KEY
#     file = "F17_udg_all"  # $COHORT
#     device = "Laptop" 
#     source = 'Aruba' #LabStat
    
    client = connectToAWS(profile)  # connect to AWS
    df = readFileCSV('Task1-NumberOfDaysPerWeek/' + file, client, source)  # Get file from AWS
    cumul = readFileCSV('Task3-CumulatedCounts/' + file + '_' + device, client, source)  # Get file from AWS
    cumul = cumul.sort_values(by=['weeks'])
    cumul = cumul[(cumul.T != 0).any()]
    print(cumul)
    stacked_plot(df, list(cumul['count']), device, source)
