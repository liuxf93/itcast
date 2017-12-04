# -*- coding:utf-8 -*-
from flask import Flask
import urllib2
import time
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
APP_ID = 'wxaebe108a59b7759a'
APP_SECRET = 'fd2dcd3c4834ed8e744ed2e4c935007d'
WECHAT_TOKEN = 'liuxiaofeng'


class AccessToken(object):
    __access_token = {
        "access_token": "",
        "update_time": time.time(),
        "expires_in": 7200
    }

    @classmethod
    def get_access_token(cls):
        if not cls.__access_token.get('access_token') or (time.time()-cls.__access_token.get('update_time') > cls.__access_token.get('expires_in')):
            url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (APP_ID, APP_SECRET)
            response = urllib2.urlopen(url)
            data = response.read()
            data_dict = json.loads(data)
            if "errcode" in data_dict:
                # 请求错误/参数有问题
                raise Exception("get accesstoken failed")

                # 设置数据
            cls.__access_token["access_token"] = data_dict.get("access_token")
            cls.__access_token["expires_in"] = data_dict.get("expires_in")
            cls.__access_token["update_time"] = time.time()
        print cls.__access_token["access_token"]
        return cls.__access_token.get('access_token')


app = Flask(__name__)


@app.route('/get_qrcode/<int:scene_id>')
def index(scene_id):
    access_token = AccessToken.get_access_token()
    # 定义url和参数
    # URL: https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=TOKENPOST
    url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s" % access_token
    # scene_id
    # json 数据格式
    # {"expire_seconds": 604800, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": 123}}}
    params = {"expire_seconds": 604800,
              "action_name": "QR_SCENE",
              "action_info": {"scene": {"scene_id": scene_id}}}
    # 将字典转成JSON字符串
    params = json.dumps(params)
    # 发起请求获取响应
    response = urllib2.urlopen(url, params)
    # 获取到响应体
    resp_data = response.read()
    # 转成字典
    resp_dict = json.loads(resp_data)
    # 获取到ticket
    ticket = resp_dict.get("ticket")

    return '<img src="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s">' % ticket


if __name__ == '__main__':
    app.run()
