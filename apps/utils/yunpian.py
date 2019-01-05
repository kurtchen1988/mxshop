import requests
import json


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        params = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text':'【陈辰网站测试】本测试网站的测试码是：{code}'.format(code=code)
        }

        response = requests.post(self.single_send_url, data=params)

        re_dict = json.loads(response.text)
        return re_dict

if __name__ == '__main__':
    yun_pian = YunPian('fbe319c5b347bb47e7578e4041a7d103')
    yun_pian.send_sms('2017','15868146400')