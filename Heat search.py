# url = http://www.boohee.com/food/group/1
# 用多协程爬取薄荷网11个常见食物分类里的食物信息（包含食物名、热量、食物详情页面链接）。
# 分类：http://www.boohee.com/food/group/+数字（1-10），http://www.boohee.com/food/view_menu
# 每类分页：
# http://www.boohee.com/food/group/ + 数字（1-10）+?page= + 数字（1-10）
# 第11类：
# http://www.boohee.com/food/view_menu?page= + 数字（1-10）

from gevent import monkey
monkey.patch_all()
import requests,gevent,csv
from bs4 import BeautifulSoup
from gevent.queue import Queue

headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}


# 网址方案二
work = Queue()
url_1 = 'http://www.boohee.com/food/group/{type}?page={page}'
for t in range(1,4):
    for p in range(1,4):
        real_url = url_1.format(type=t,page=p)
        work.put_nowait(real_url)

url_2 = 'http://www.boohee.com/food/view_menu?page={page}'
for p in range(1,4):
    real_url = url_2.format(page=p)
    work.put_nowait(real_url)

        

# 网址方案一
# url_list = []
# for g in range(3):
#     url_1 = 'http://www.boohee.com/food/group/'+str(g+1)
#     for p in range(3):
#         url = url_1 + '?page=' + str(p+1)
#         url_list.append(url)
#     url_2 = 'http://www.boohee.com/food/view_menu?page=' +str(g+1)
#     url_list.append(url_2)

# work = Queue()
# for url in  url_list:
#     work.put_nowait(url)

# 待扩展
foods_list = []
def crawler():
    while not work.empty():
        url= work.get_nowait()
        r = requests.get(url,headers=headers)
        soup = BeautifulSoup(r.text,'html.parser')
        item_tags = soup.find_all('div',class_='text-box')
        for item in item_tags:
            name_tag = item.find('a')
            name = name_tag.text
            link = 'http://www.boohee.com/'+name_tag['href']

            heat_tag = item.find('p')
            heat = heat_tag.text
            # print(heat_tag)
            foods_list.append([name,heat,link])
    return foods_list


tasks_list = []
for x in range(2):
    task = gevent.spawn(crawler)
    tasks_list.append(task)

gevent.joinall(tasks_list)

# csv存档
with open('Bohewang.csv','w',newline='',encoding='utf-8') as f:
    writer =csv.writer(f)
    writer.writerow(['食物','热量','详情链接'])
    writer.writerows(foods_list)

print('程序已完成！')
