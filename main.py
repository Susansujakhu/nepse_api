from cmath import sqrt
import math
from numpy import index_exp
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv

# open the file in the write mode
f = open('output.csv', 'w')

# create the csv writer
writer = csv.writer(f)

file_header = [
    'Company Name',
    'Sector', 
    'Market Price', 
    '52 Weeks High - Low', 
    'EPS', 
    'P/E Ratio', 
    'Book Value', 
    'PBV', 
    '% Dividend',
    '% Bonus',
    'Right Share',
    'G.N', 
    'price above GN', 
    ]

writer.writerow(file_header)

url = "https://merolagani.com/LatestMarket.aspx"

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html5lib')

main_table = soup.find('table', attrs={'class':'live-trading'}).find('tbody')


for row in main_table.find_all('tr'):
    data = row.find('td').find('a').text
    url = "https://merolagani.com/CompanyDetail.aspx?symbol="+data
    print(url)

    page=requests.get(url)

    soup = BeautifulSoup(page.content, 'html5lib')

    main_table = soup.find('table', attrs={'id':'accordion'})

    company_name = soup.find('span', attrs={'id':'ctl00_ContentPlaceHolder1_CompanyDetail1_companyName'}).text

    indexed_row = [company_name]
    # print(main_table.prettify())
    # print(main_table.find_all('tr'))

    for row in main_table.find_all('tr'):
        position = file_header.index('PBV')

        try:
            fetched_data = str(row.find('th').text).strip()
            if fetched_data in file_header:
                indexed_row.append(str(row.find('td').text).strip())
            
        except:
            continue

    G_N_index = file_header.index('G.N')
    price_above_G_N_index = file_header.index('price above GN')


    eps = indexed_row[4].replace(',','')[0:4:1]
    indexed_row[4] = eps
    book_value = indexed_row[6].replace(',','')
    try:
        indexed_row.append(math.sqrt(22.5*float(eps)*float(book_value)))
    except:
        indexed_row.append('0')
        
    ltp = indexed_row[2].replace(',','')

    try:
        indexed_row.append((float(ltp)-float(indexed_row[11]))/float(indexed_row[11])*100)
    except:
        indexed_row.append(0)
    writer.writerow(indexed_row)

f.close()





# df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings}) 
# df.to_csv('products.csv', index=False, encoding='utf-8')