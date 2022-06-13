import requests
import re
import json


# 初始化全局变量
AppKey = ""  # apikey
SecretKey = ""
SignKey = ""
redirect_uri = 'oob'  # 默认回调地址
payload = {}
headers = {'User-Agent': 'pan.baidu.com'}

# 流程:
# 1 需要引导用户授权，获取授权code
url_user = 'http://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id=' + AppKey + '\
&redirect_uri=' + redirect_uri + '&scope=basic,netdisk&display=popup&qrcode=1&force_login=1&device_id=820921428tp8x63q51'
url_user

code = ''

# 2 用code换取Access_token
url_access_token = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=authorization_code&code=' + code + '&client_id=' + AppKey + '&\
client_secret=' + SecretKey + '&redirect_uri=' + redirect_uri
req = requests.get(url_access_token)
req_contant = req.text
req_contant = json.loads(req_contant)


# 将access_token等参数存入字典并写入文件以复用
acc_dict = dict([('access_token', req_contant['access_token']), ('expires_in',
                                                                 req_contant['expires_in']/3600/24), ('refresh_token', req_contant['refresh_token'])])
acc_json = json.dumps(acc_dict, indent=4, ensure_ascii=False, sort_keys=True)
with open('pan.json', 'w') as file:
    file.write(acc_json)

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------
# 从本地文件中获取access_token等变量的值

with open('pan.json', 'r') as file:
    acc_json = file.read()
    acc_dict = json.loads(acc_json)
    access_token = acc_dict['access_token']


# 3 登陆用户的网盘
url_pan = 'https://pan.baidu.com/rest/2.0/xpan/nas?access_token=' + \
    access_token + '&method=uinfo'
inf = requests.request("GET", url_pan, headers=headers, data=payload)
inf.cont = json.loads(inf.text)
inf.json = json.dumps(inf.cont, ensure_ascii=False, indent=4, sort_keys=True)

# 获取网盘容量信息
url_quota = 'https://pan.baidu.com/api/quota?access_token=' + \
    access_token + '&checkfree=0&checkexpire=0'
quota = requests.get(url_quota)
quota.cont = json.loads(quota.text)
quota.json = json.dumps(quota.cont, ensure_ascii=False,
                        indent=4, sort_keys=True)

# 获取文件列表
url_file = 'https://pan.baidu.com/rest/2.0/xpan/file?method=list&dir=/我的资源&order=time&start=0&limit=10&web=web&folder=0&access_token='+access_token+'&desc=1'
file = requests.request("GET", url_file, headers=headers, data=payload)
file.cont = json.loads(file.text)
file.json = json.dumps(file.cont, ensure_ascii=False, indent=4, sort_keys=True)

# 获取文件名列表
list_a = []
for i in file.cont['list']:
    list_a.append(i['server_filename'])
# 获取对应的fs_id
list_b = []
for i in file.cont['list']:
    list_b.append(i['fs_id'])
# 存入文件字典
files = {}
for i in range(len(list_a)):
    files[list_a[i]] = list_b[i]

# 获取文件信息
url_filemetas = 'http://pan.baidu.com/rest/2.0/xpan/multimedia?access_token=' + \
    access_token + '&method=filemetas&fsids=' + \
    '[930117730396832]' + '&thumb=1&dlink=1&extra=1'
filemetas = requests.request("get", url_filemetas)
filemetas.cont = json.loads(filemetas.text)
filemetas.json = json.dumps(
    filemetas.cont, indent=4, ensure_ascii=False, sort_keys=True)

# 从文件信息中取出下载地址dlink
dlink = filemetas.cont['list'][0]["dlink"]

# 用access_token和dlink进行下载操作
url_dlinkacc = dlink + '&access_token=' + access_token
dlinkacc = requests.request("get", url_dlinkacc, headers=headers, data=payload)
with open('123.pptx', 'wb') as code:
    code.write(dlinkacc.content)
