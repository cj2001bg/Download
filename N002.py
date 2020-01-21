import requests,csv
from bs4 import BeautifulSoup

infos = []
for k in range(5):
    URL = 'http://www.bjxty.com/columnss19-'+str(k) +'.html'
    
    res = requests.get(URL)
    # print(res.status_code)
    soup = BeautifulSoup(res.text,'html.parser')
    soups = soup.find_all('span',class_='buy_Button')
    price_tags = soup.find_all('span',class_='price')

    for i in range(len(soups)):
        name_tag = soups[i].find('input',class_='column_Comparison')
        name = name_tag['onclick']

        price = price_tags[i].text
        infos.append([name,price])
        
with open('Bloodpaperlist.csv','w',encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerows(infos)
print('写入完毕！')


