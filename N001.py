# 我们分别提取所有的菜名、所有的URL、所有的食材。然后让菜名、URL、食材给一一对应起来。
# URL:http://www.xiachufang.com/explore/
# list1 = ['caiming1','caiming2','caiming3',...]
# list2 = [URL1,URL2,URL3,...]
# list3 = ['shicai1','shicai2','shicai3',...]
# list_all = [(list1[0],list2[0],list3[0]),(list1[1],list2[1],list3[1]),(list1[2],list2[2],list3[2]),(list1[i],list2[i],list3[i])]
import requests,csv
from bs4 import BeautifulSoup

res = requests.get('http://www.xiachufang.com/explore/')
# print(res.status_code)
html = res.text
soup = BeautifulSoup(html,'html.parser')

list_foods = soup.find_all(class_='info pure-u')    # 父级标签
n = len(list_foods)

list_all =[]
list_names = []
list_URLs =[]
list_ings = []
for i in range(n):
    list_name = list_foods[i].find('a')                 # 子级，菜名
    name = list_name.text.strip()
    list_names.append(name)

    list_URL = list_name['href']                        # 子级，URL
    URL = 'http://www.xiachufang.com/' + list_URL
    list_URLs.append(URL)

    list_ing = list_foods[i].find(class_='ing ellipsis')    # 子级，食材
    ing = list_ing.text.strip()
    list_ings.append(ing)

for i in range(n):
    list_all.append([list_names[i],list_ings[i],list_URLs[i]])  

with open('Foodslist.csv','w',encoding='utf-8') as f:     #window用'utf-8-sig'
    writer = csv.writer(f)
    writer.writerows(list_all)

print('写入完毕！')
