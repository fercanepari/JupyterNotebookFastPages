# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 16:15:18 2021

@author: CanepariF
"""

#import streamlit as st
import requests

base_url = 'https://fercanepari.pythonanywhere.com/notes'


# Call API
response = requests.get(base_url)
#print(r.content)

#print(response.content) # Raw data.
#print(response.status_code) # Status code.
#print(response.headers) # Content type.
#print(response.headers['Content-Type']) # Content type.
#print(response.text)
#print(response.json)
r_dictionary = response.json()


for i in response.json():
    #print(i)
    #print(r_dictionary[i])
    for j in r_dictionary[i]:
        print(r_dictionary[i][j])
        ##print(j)
        
    print("---")


#for i in response:
    #title = i['title']
    #print(i)
    #print("---")





