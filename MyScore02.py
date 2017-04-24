# 抓取成绩
# Author:hugo
# email:hugooood@outlook.com
# Time:2017/4/24

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path
try:
    from PIL import Image
except:
    pass

# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
headers = {
    "Host": "218.59.189.229",
    "Referer": "http://218.59.189.229/",
    "User-Agent": agent,
    "lt":"LT-28423-DSlOft79B2kPGLenaaxewJTOhAKh1S",
    "execution":"e1s1",
    "service":"http://218.59.189.229/login"
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")

def get_lt():
    '''_lt 是一个动态变化的参数'''
    index_url = 'http://218.59.189.229/login'
    # 获取登录时需要用到的_lt
    index_page = session.get(index_url, headers=headers)
    html = index_page.text
    pattern = r'name="lt" value="(.*?)"'
    # 这里的_lt 返回的是一个list
    _lt = re.findall(pattern, html)
    return _lt[0]

# 获取验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'http://218.59.189.229/cas/getVerificationCode?dateTime=' + t
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha

# def isLogin():
#     # 通过查看用户个人信息来判断是否已经登录
#     url = "http://218.59.189.226/jsxsd/kscj/cjcx_query?Ves632DSdyV=NEW_XSD_XJCJ"

#     postdata = {
#              "password": password,
#              "username": username,
#              "vcode":get_captcha(),          
#              "_eventId":"submit",
                
#     }      

#     login_page = session.get(url, headers=headers, allow_redirects=False)
#     with open('text1.txt', 'wb') as f:
#         f.write(login_page.content)

#     login_code = session.get(url,headers=headers, allow_redirects=False).status_code
    
#     if login_code == 200:
        
#         return True
#     else:
#         print(login_code)
#         print('False')
#         return False

def login(username, password):
    post_url = "http://218.59.189.229/cas/login?service=http%3A%2F%2F218.59.189.229%2Flogin"
    postdata = {
             "password": password,
             "username": username,
             "vcode":get_captcha(),
             "execution":"e1s1",
             "_eventId":"submit",
             "lt":get_lt()    
    }
    login_page = session.post(post_url, data=postdata,headers=headers)
    
    session.cookies.save()



if __name__ == '__main__':

    username = input('请输入你的用户名\n>  ')
    password = input("请输入你的密码\n>  ")
    login(username, password)
    login_page = session.get("http://218.59.189.226/jsxsd/kscj/cjcx_list")
    #保存数据
    with open('text1.txt', 'wb') as f:
        f.write(login_page.content)
