#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 22:37:16 2024

@author: ginabarbagallo
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display, Markdown

ETL = pd.read_csv('/Users/ginabarbagallo/Downloads/EPL.csv')

print(ETL.head())
print(ETL.info())

epl_condensed = ETL[['Season','Team','Pos','Pts','GF','GD', 'Qualification or relegation']]

def update_result(result):
    if 'Champions League' in result:
        result = 'Champions League'
    elif 'Europa' in result or 'UEFA' in result:
        result = 'Europa'
    elif 'Relegation' in result: 
        result = 'Relegated'
    else:
        result = '-'
    return result

epl_condensed = epl_condensed.rename(columns = {'Qualification or relegation' : 'Result'})

epl_condensed['Result'] = epl_condensed['Result'].apply(update_result)

print(epl_condensed['Result'].value_counts())

cl_qual = epl_condensed[epl_condensed.Result == 'Champions League']

cl_qual_stats = cl_qual\
                .groupby('Season')\
                .agg({'Pos':'max', 'Pts':'min', 'GD':'min'})      
                
print(cl_qual_stats)

el_qual = epl_condensed[epl_condensed.Result == 'Europa']

el_qual_stats = el_qual\
                .groupby('Season')\
                .agg({'Pos':'max', "Pts":'min', 'GD':'min'})
                
print(el_qual_stats)

epl_winners = epl_condensed[epl_condensed['Pos'] == 1]
epl_winners = epl_winners.reset_index(drop=True)

relegation_zone = epl_condensed[epl_condensed['Pos']==18]
relegation_zone = relegation_zone.reset_index(drop=True)

plt.figure(figsize=(12,6))

sns.lineplot(x='Season',y="Pts", data=relegation_zone, marker = 'o',
             color = '#e12345', label = 'relegation')

sns.lineplot(x='Season', y='Pts', data=epl_winners, marker='o', color='#38003c', label='winner')

plt.xticks(rotation=90)

plt.title('Points of EPL Winners & Relegated Teams')
plt.xlabel('Season')
plt.ylabel('Points')

plt.show()

team_counts = epl_condensed['Team'].value_counts()

euro_ids = epl_condensed['Result'].isin(['Europa','Champions League'])

euro_year_counts = epl_condensed[euro_ids]['Team'].value_counts()

plt.figure(figsize=(12,6))

sns.barplot(data=team_counts, color='#38003c')

plt.ylabel('Years in EPL')

plt.xticks(rotation=90)

plt.show()

chelsea = epl_condensed[epl_condensed.Team == 'Chelsea']

# Set figure size
plt.figure(figsize=(12, 6))

ax = sns.lineplot(x='Season', y='GD', data=chelsea, label='Goal Diff.', marker='o')
ax2 = ax.twinx()
sns.lineplot(x='Season', y='Pts', data=chelsea, label='Points', ax=ax2, marker='o', color='green')

lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax.legend(lines + lines2, labels + labels2, loc='upper left')

ax2.get_legend().remove()

ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

plt.title("Chelsea GD and Pts per season")
plt.show()