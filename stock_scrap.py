from datetime import date
import requests
from bs4 import BeautifulSoup as bs
import csv
import os

today = date.today()
file_name = f'{str(today)}.csv'
file_path = '/tmp/Stock/Data/'

def stock_scrap(url):
    response = requests.get(url)
    content = response.content
    soup = bs(content,features="html.parser")
    tds = soup.find_all("td") #find table data
    data_list = [td.text.replace('\xa0', '').replace(',', '.').replace('\n', '') for td in tds] #clean out data from tds
    data_list.remove('') #clean out data pt2
    return data_list

#GPW
url = 'https://www.bankier.pl/gielda/notowania/akcje'
data = stock_scrap(url)
data_rows = [[str(today), 'GPW'] + data[i:i+10] for i in range(0, len(data), 10)] #put data list into rows

#NC
url = 'https://www.bankier.pl/gielda/notowania/new-connect'
data = stock_scrap(url)
data_rows += [[str(today), 'NC'] + data[i:i+10] for i in range(0, len(data), 10)] #append to the data list with rows

#create file
with open(f'{file_path}{file_name}', 'a', newline='') as file:
    writer = csv.writer(file)
    for row in data_rows:
        writer.writerow(row)

#copy file from temp to an archive
os.system(f'cp {file_path}{file_name} /home/pi/Stock/Data/{file_name}')