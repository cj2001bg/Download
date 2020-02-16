import requests,smtplib,schedule,time
from email.mime.text import MIMEText
from email.header import Header
from bs4 import BeautifulSoup

account = input('请输入你的邮箱：')
password = input('请输入你的密码：')
receiver = input('请输入收件人的邮箱：')

def weather_spider():
    headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    url='http://www.weather.com.cn/weather/101280601.shtml'

    res = requests.get(url,headers=headers)
    res.encoding = 'utf-8'

    if res.status_code == 200:
        bs = BeautifulSoup(res.text,'html.parser')
        data1 = bs.find('p',class_='tem')
        data2 = bs.find('p',class_='wea')
        tem = data1.text.strip()
        wea = data2.text
        return tem,wea

def send_mail(tem,weather):
    # 把邮箱的服务器地址赋值到变量mailhost上，地址需要是字符串的格式。
    mailhost = 'smtp.163.com'
    #实例化一个smtplib模块里的SMTP类的对象，这样就可以使用SMTP对象的方法和属性了
    mail_163 = smtplib.SMTP(mailhost)
    #连接服务器，第一个参数是服务器地址，第二个参数是SMTP端口号。
    mail_163.connect(mailhost,465)
    #以上，皆为连接服务器的代码

    mail_163.login(account,password)

    #输入你的邮件正文
    content = '亲爱的，今天的天气是：'+tem+weather
    #实例化一个MIMEText邮件对象，该对象需要写进三个参数，分别是邮件正文，文本格式和编码.
    message = MIMEText(content,'plain','utf-8-sig')
    #用input()获取邮件主题  
    subject = '今日天气预报'
    #在等号的右边，是实例化了一个Header邮件头对象，该对象需要写入两个参数，分别是邮件主题和编码，然后赋值给等号左边的变量message['Subject']。
    message['Subject'] = Header(subject,'utf-8')

    try:
        #发送邮件，调用了sendmail()方法，写入三个参数，分别是发件人，收件人，和字符串格式的正文。
        mail_163.sendmail(account,receiver,message.as_string())
        print('邮件发送成功')
    except:
        print('邮箱发送失败')
    #退出邮箱
    mail_163.quit()

def job():
    print('开始一次任务')
    tem,weather = weather_spider()
    send_mail(tem,weather)
    print('任务完成')

schedule.every().day.at("07:30").do(job)
# schedule.every(10).minutes.do(job)                  #部署每10分钟执行一次job()函数的任务
# schedule.every().hour.do(job)                       #部署每×小时执行一次job()函数的任务
# schedule.every().day.at("10:30").do(job)            #部署在每天的10:30执行job()函数的任务
# schedule.every.monday.do(job)                       #部署每个星期一执行job()函数的任务
# schedule.every().wednesday.at("13:15").co(job)      #部署每周三的13：15执行函数的任务

while True:
    schedule.run_pending()
    time.sleep(1)
# 如果任务准备就绪，就开始执行任务。
