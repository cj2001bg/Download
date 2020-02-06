import requests,json

session = requests.session()
#创建会话。
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}
# 登录的网址
url_signin = ' https://wordpress-edu-3autumn.localprod.oc.forchange.cn/wp-login.php'
# 文章的网址
url_usage = 'https://wordpress-edu-3autumn.localprod.oc.forchange.cn/wp-comments-post.php'
# 评论网址
url_post = 'https://wordpress-edu-3autumn.localprod.oc.forchange.cn/wp-comments-post.php'

# 函数功能：读取存储好的cookies
def cookies_read():
    # 读取已存在文件中的cookies,此时为字符串形式
    cookies_txt = open('cookies.txt','r')
    # 利用json将cookies转换成字典
    cookies_dict = json.loads(cookies_txt.read())
    # 将cookies从字典形式转换为cookies正常形式
    cookies = requests.utils.cookiejar_from_dict(cookies_dict)
    # 返回cookies，给后面session用
    return(cookies)

# 函数功能：登录网站
def sign_in():
    # 登录的参数
    data = {'log': input('请输入你的账号:'),
            'pwd': input('请输入你的密码:'),
            'wp-submit': '登录',
            'redirect_to': 'https://wordpress-edu-3autumn.localprod.oc.forchange.cn',
            'testcookie': '1'}
    # 在会话下，用post发起登录请求
    session.post(url_signin,headers=headers,data=data)
    # 将session中的cookies提取出来，此时为字典
    cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
    # 利用json将cookies转换为字符串
    cookies_str = json.dumps(cookies_dict)
    # 存储cookies信息，将字符串格式的cookies存成txt文件
    with open('cookies.txt','w') as f:
        f.write(cookies_str)

# 函数功能：发布评论
def write_message():
    # 评论的参数
    data_2 = {
            'comment': input('请输入你想评论的内容：'),
            'submit': '发表评论',
            'comment_post_ID': '13',
            'comment_parent': '0'
}
    # 在创建的会话session下，用post发布评论
    return(session.post(url_post,headers=headers,data=data_2))

# 先读取已存储的cookies，用于后面的发布评论
try:
    # 调用函数，读取cookies
    session.cookies = cookies_read()
# 若没有已存储的cookies，在调用登录函数，存取cookies
except FileNotFoundError:
    sign_in()
    # 读取已存储的cookies，用于后面的发布评论
    session.cookies = cookies_read()

# 发布评论
# 将会话session下用post发布的评论赋值给num
num = write_message()
# 根据返回的状态码，判断cookies是否过期了
# 若为200，则发布成功
if num.status_code == 200:
    print('成功了！')
# 若不是200，则表示cookies过期了，要重新登录
else:
    sign_in()
    session.cookies = cookies_read()
    num = write_message()
    print('成功了！')
