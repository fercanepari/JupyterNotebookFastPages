# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 10:56:01 2021

@author: CanepariF
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://webscraper.io/test-sites/tables"

html_code = urlopen(url).read().decode('utf-8')

#print(html_code)
#start = html_code.find("<h1>") + len("<h1>")
#end = html_code.find("</h1>") 
#print(html_code[start:end])

soup = BeautifulSoup(html_code, 'lxml')

headings_2 = soup.find_all("h2")
print(headings_2)

images = soup.find_all("img")

print(images[1]['src'])


first_table = soup.find('table')
rows = first_table.find_all('tr')[1:]

last_names = []

for row in rows:
    last_names.append(row.find_all('td')[2].get_text())
    
print(last_names)    
    


