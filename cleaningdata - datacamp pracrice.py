#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 23:02:13 2024

@author: ginabarbagallo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#read the data

audible = pd.read_csv('/Users/ginabarbagallo/Downloads/audible_raw.csv')

print(audible.head())

#inspect the data types
print(audible.info())

# Remove Writtenby: from the author column
audible['author'] = audible['author'].str.replace('Writtenby:', '')
# Remove Narratedby: from the narrator column
audible['narrator'] = audible['narrator'].str.replace('Narratedby:', '')
# Check the results
print(audible['author'].head())
print(audible['narrator'].head())

# Explore the values of the star column that are not 'Not rated yet'
print(audible['stars'].value_counts())

# Replace 'Not rated yet' with NaN
audible['stars'] = np.where(audible['stars'] == 'Not rated yet', np.nan, audible['stars'])
print(audible['stars'].value_counts())

# Extract number of stars into rating_stars and turn into float
audible['rating_stars'] = audible['stars'].str.extract(r'(\d+\.\d+|\d+)').astype(float)

# Replace the comma, extract number of ratings into n_ratings and turn into float
audible['n_ratings'] = audible['stars'].str.extract(r'(\d+(?:,\d{3})*) ratings')[0].str.replace(',', '').astype(float)

# Examine the new rating_stars and n_ratings columns
audible[['rating_stars', 'n_ratings']]

# Explore the price column
print(audible['price'].head())

# Replace the comma with ''
audible['price'] = audible['price'].str.replace(",", '')

# Replace 'Free' with 0
audible['price'] = audible['price'].str.replace('Free', '0')

# Turn price to float
audible['price'] = audible['price'].astype('float')

# Look at the unique values in the rating_stars column
audible['rating_stars'].unique()

# Turn rating_stars to category
audible['rating_stars'] = audible['rating_stars'].astype('category')

# Convert releasedate to datetime
audible['releasedate'] = pd.to_datetime(audible['releasedate'])

# Inspect the dataframe
audible.info()

# Replace hrs, mins, and 'Less than 1 minute'
audible['time'] = audible['time'].str.replace('hrs', 'hr')
audible['time'] = audible['time'].str.replace('mins', 'min')
audible['time'] = audible['time'].str.replace('Less than 1 minute', '1 min')

# Extract the number of hours, turn to integer
audible['hours'] = audible['time'].str.extract(r'(\d+)\s*hr').fillna(0).astype(int)

# Extract the number of minutes, turn to integer
audible['mins'] = audible['time'].str.extract(r'(\d+)\s*min').fillna(0).astype(int)

# Combine hours and minutes into the time_mins column
audible['time_mins'] = audible['hours'] * 60 + audible['mins']

# Check the results
audible[['time', 'hours', 'mins', 'time_mins']].head()

#plot numerical columns

# Select numerical columns
numerical_columns = audible.select_dtypes(include=['int64', 'float64'])

# Plot histograms
numerical_columns.hist(bins=30, figsize=(15, 10))
plt.show()

# Transform prices to USD (multiply times 0.012)
audible['price'] = audible['price'] * 0.012
# Check the results
print(audible['price'].head())

# Update capitalization in the language column
audible['language'] = audible['language'].str.lower()
audible['language'].str.replace('English', 'english')
audible['language'].str.replace('Hindi', 'hindi')

print(audible['language'].unique())

# Create a list of our subset columns and assign to subset_cols
subset_cols = ['name', 'author', 'narrator', 'time_mins', 'price']
# Check for duplicates using our subset of columns
audible.duplicated(subset=subset_cols).sum()

# Check the duplicated rows keeping the duplicates and order by the name column
duplicates = audible[audible.duplicated(subset=subset_cols, keep=False)]
duplicates_sorted = duplicates.sort_values(by='name')
duplicates_sorted

# Drop duplicated rows keeping the last release date
audible = audible.drop_duplicates(subset=subset_cols, keep='last')

# Check for null values
audible.isna().sum()

