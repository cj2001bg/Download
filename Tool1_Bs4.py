#用BS4解析数据，提取数据

import requests
from bs4 import BeautifulSoup
# URL为目标网址
headers={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
URL = 'https://localprod.pandateacher.com/python-manuscript/crawler-html/spider-men5.0.html'
res = requests.get(URL,headers=headers)

if res.status_code == 200:
    soup = BeautifulSoup(res.text,'html.parser')
# 缩小搜索范围：soup.find，soup.find_all,soup.标签名,...
# 精确提取信息：tag.text文本内容；tag['属性名']，正则，字符串处理等方式
# 存储到文件：
# 1.存成列表 
# 2.with open('文件名.后缀','打开方式') as file:
# 3. file.write(列表) 
# 4. print('写入完毕')

    items = soup.find_all(class_='books')
    for item in items:
        kind = item.h2
        title = item.find(class_='title')
        brief = item.find(class_='info')
        print(kind.text)
        print(title.text)
        print(title['href'])
        print(brief.text)
    

