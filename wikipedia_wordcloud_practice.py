# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 08:43:28 2021

@author: Raghu
"""

import wikipedia

#Creating a function to get desired data from wikipedia
def get_wiki(query):
    title = wikipedia.search(query)[0]
    page = wikipedia.page(title)
    return page.content

print (get_wiki("IIT Bhubaneswar"))

from wordcloud import WordCloud, STOPWORDS

stopword = set(STOPWORDS)
    
wc = WordCloud(width = 800, height = 800, 
                   background_color="White",
                   mask=None,
                   max_words=400,
                   stopwords=stopword,
                   min_font_size = 10).generate(get_wiki("IIT Bhubaneswar"))

wc.to_file("F:/pyWork/pyData/WC_IITB.png")