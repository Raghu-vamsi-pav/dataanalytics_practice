# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 08:40:53 2021

@author: Raghu
"""

#Import Libraries----------
import numpy as np 
import pandas as pd 
from mlxtend.frequent_patterns import apriori, association_rules 

#Loading and exploring the data-----------------
#Loading the Data 
data = pd.read_excel('Online_Retail_Store.xlsx') 
data.head() 
data.info()
# Exploring the columns of the data 
data.columns 
# Exploring the different regions of transactions 
data.Country.unique() 

#Cleaning the Data-----------------
#Identifying missing values:
'''Is there any missing values across columns'''
data.isnull().any()

'''How many missing values are there across each column'''
data.isnull().sum()

# Dropping the rows without any invoice number 
data.dropna(axis = 0, subset =['InvoiceNo'], inplace = True) 
data.isnull().sum()

# Dropping all transactions which were done on credit
data.info() 
data = data[~data['InvoiceNo'].str.contains('C')]
#For the above cmd to work, we need to ensure that we convert Column "Invoinve No." to string form.
data['InvoiceNo'] = data['InvoiceNo'].astype('str') 
data = data[~data['InvoiceNo'].str.contains('C')] 
#Hence, now we have been able to remove the rows with credit (C) type billing.

# Stripping extra spaces in the description 
data['Description'] = data['Description'].str.strip() 

#Splitting the data according to the region of transaction-------
# Transactions done in France 
basket_France = (data[data['Country'] =="France"] 
		.groupby(['InvoiceNo', 'Description'])['Quantity'] 
		.sum().unstack().reset_index().fillna(0) 
		.set_index('InvoiceNo')) 

# Transactions done in the United Kingdom 
basket_UK = (data[data['Country'] =="United Kingdom"] 
		.groupby(['InvoiceNo', 'Description'])['Quantity'] 
		.sum().unstack().reset_index().fillna(0) 
		.set_index('InvoiceNo')) 

# Transactions done in Portugal 
basket_Por = (data[data['Country'] =="Portugal"] 
		.groupby(['InvoiceNo', 'Description'])['Quantity'] 
		.sum().unstack().reset_index().fillna(0) 
		.set_index('InvoiceNo')) 

basket_Sweden = (data[data['Country'] =="Sweden"] 
		.groupby(['InvoiceNo', 'Description'])['Quantity'] 
		.sum().unstack().reset_index().fillna(0) 
		.set_index('InvoiceNo')) 

#Hot encoding the Data------------
# Defining the hot encoding function to make the data suitable 
# for the concerned libraries 
def hot_encode(x): 
	if(x<= 0): 
		return 0
	if(x>= 1): 
		return 1

# Encoding the datasets 
basket_encoded = basket_France.applymap(hot_encode) 
basket_France = basket_encoded 

basket_encoded = basket_UK.applymap(hot_encode) 
basket_UK = basket_encoded 

basket_encoded = basket_Por.applymap(hot_encode) 
basket_Por = basket_encoded 

basket_encoded = basket_Sweden.applymap(hot_encode) 
basket_Sweden = basket_encoded 

#Building the models and analyzing the results-----------------

#France:
# Building the model 
frq_items = apriori(basket_France, min_support = 0.05, use_colnames = True) 
frq_items

# Collecting the inferred rules in a dataframe 
rules = association_rules(frq_items, metric ="lift", min_threshold = 1) 
print(rules.head()) 
France_rules=pd.DataFrame(rules)

#Portugal
frq_items = apriori(basket_Por, min_support = 0.05, use_colnames = True) 
rules = association_rules(frq_items, metric ="lift", min_threshold = 1) 
print(rules.head()) 
Portugal_rules=pd.DataFrame(rules)

#Sweden
frq_items = apriori(basket_Sweden, min_support = 0.05, use_colnames = True) 
rules = association_rules(frq_items, metric ="lift", min_threshold = 1) 
print(rules.head()) 
Sweden_rules=pd.DataFrame(rules)

#UK
frq_items = apriori(basket_UK, min_support = 0.05, use_colnames = True) 
rules = association_rules(frq_items, metric ="lift", min_threshold = 1) 
print(rules.head()) 
UK_rules=pd.DataFrame(rules)

#Here Empty DataFrame signifies that none of the Rules in UK satisfy the levels mentioned for 
#Support & Lift in above freq items sets
 
def draw_graph(rules, rules_to_show):
  import matplotlib.pyplot as plt
  import networkx as nx  
  G1 = nx.DiGraph()
   
  color_map=[]
  N = 50
  colors = np.random.rand(N)    
  strs=['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16']   
   
   
  for i in range (rules_to_show):      
    G1.add_nodes_from(["R"+str(i)])
    
     
    for a in rules.iloc[i]['antecedents']:
                
        G1.add_nodes_from([a])
        
        G1.add_edge(a, "R"+str(i), color=colors[i] , weight = 2)
       
    for c in rules.iloc[i]['consequents']:
             
            G1.add_nodes_from([c])
            
            G1.add_edge("R"+str(i), c, color=colors[i],  weight=2)
 
  for node in G1:
       found_a_string = False
       for item in strs: 
           if node==item:
                found_a_string = True
       if found_a_string:
            color_map.append('yellow')
       else:
            color_map.append('green')       
 
 
   
  edges = G1.edges()
  colors = [G1[u][v]['color'] for u,v in edges]
  weights = [G1[u][v]['weight'] for u,v in edges]
 
  pos = nx.spring_layout(G1, k=16, scale=1)
  nx.draw(G1, pos, edges=edges, node_color = color_map, edge_color=colors, width=weights, font_size=16, with_labels=False)            
   
  for p in pos:  # raise text positions
           pos[p][1] += 0.07
  nx.draw_networkx_labels(G1, pos)
  plt.show()
 
 
#Chart showing association rules of few products frequently sold in France    
fig_1 = draw_graph (France_rules, 10)
fig_1

#Chart showing association of few products frequently sold in Portugal    
fig_2 = draw_graph (Portugal_rules, 10)
fig_2

#Chart showing association of few products frequently sold in Sweden    
fig_3 = draw_graph (Sweden_rules, 5)
fig_3

#Chart showing association of few products frequently sold in UK 
fig_4 = draw_graph (UK_rules, 5)
fig_4

#Note: We get an error here in case of "UK" bcz none of the product associations in UK
# follow the criteria of min support = 0.05 mentioned above in line:
# frq_items = apriori(basket_UK, min_support = 0.05, use_colnames = True) 
