# 带参数请求
import requests

url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg'
# 伪装头
headers = {
    'origin':'https://y.qq.com',
    # 请求来源，本案例中其实是不需要加这个参数的，只是为了演示
    'referer':'https://y.qq.com/n/yqq/song/004Z8Ihr0JIu5s.html',
    # 请求来源，携带的信息比“origin”更丰富，本案例中其实是不需要加这个参数的，只是为了演示
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    # 标记了请求从什么设备，什么浏览器上发出
    }

for i in range(5):
        # 把header里面的Query String Parameters封装成字典
        # 要给他们打引号，让它们变字符串。用逗号隔开,去掉空格
        params = {
                'g_tk':'5381',
                'loginUin':'0',
                }
        # 带参数请求
        res = requests.get(url,headers=headers,params=params)

        if res.status_code == 200:
                json_comments = res.json()
                list_comments = json_comments['comment']['commentlist']
                
                for coment in list_comments:
                        print(coment['rootcommentcontent'])
                        print('----------------------------')
