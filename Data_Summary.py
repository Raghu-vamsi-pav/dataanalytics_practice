# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 12:29:05 2020

@author: Raghu
"""
#-------------------------------Data Summary-------------------------------
#Describe()- Used to get summary statistics in python.
#Describe Function gives the mean, std and IQR values.
#It analyzes both numeric and object series and also the DataFrame column sets of mixed data types.
# creation of DataFrame
import pandas as pd

#Example 1:
a1 = pd.Series([1, 2, 3, 4]) 
a1 
a1.describe()  

a2 = pd.Series(['q', 'r', 'r', 'r', 'q', 's', 'p'])  
a2
a2.describe() 

info = pd.DataFrame({'numeric': [1, 2, 3, 4],  
'object': ['p', 'q', 'r','e']  
 })  
info


#Example 2:
#Create a Dictionary of series
d = {'Name':pd.Series(['Cathrine','Alisa','Bobby','Madonna','Rocky','Sebastian','Jaqluine',
                       'Rahul','David','Andrew','Ajay','Teresa']),
'Age':pd.Series([26,27,25,24,31,27,25,33,42,32,51,47]),
'Score':pd.Series([89,87,67,55,47,72,76,79,44,92,99,69])}

#Create a DataFrame
df = pd.DataFrame(d)
print (df)

#Descriptive or Summary Statistic of the numeric columns:
#Summary statistics
print(df.describe())

#Descriptive or Summary Statistic of the character columns:
#Summary statistics of character column
print(df.describe(include='object'))

#Descriptive or Summary Statistic of all the columns
#Summary statistics of both - character & numerical columns
print(df.describe(include='all'))
#--------------------------------------------------------------------------------------------------------------- 
