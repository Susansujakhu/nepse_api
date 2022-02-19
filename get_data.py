from cmath import sqrt
import math
from bs4 import BeautifulSoup
from numpy import single
import requests


url = "https://www.sharesansar.com/today-share-price"

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html5lib')

main_table = soup.find('table', attrs={'id':'headFixed'})

table_head = main_table.find('thead')

table_data = main_table.find('tbody')

data_header = []

for head_value in table_head.find_all("th"):
    data_header.append(head_value.text)

single_data = {}

all_data = []


for data_value in table_data.find_all("tr"):
    single_data = {}
    i = 0
    for data in data_value.find_all("td"):
        if i == 1:
            single_data['Company Name'] = single_data.pop('S.No')
            single_data['Company Name'] = data.find('a')['title']

        single_data.update({data_header[i] : data.text.strip()})
        i+=1
    all_data.append(single_data)
print(all_data)
