

def get_auth_url():
    weibo_auth_url = 'https://api.weibo.com/oauth2/authorize'
    redirect_url = 'http://127.0.0.1:8080/complete/weibo'
    auth_url = weibo_auth_url+'?client_id={client_id}&redirect_url={re_url}'.format(client_id=123456, re_url=redirect_url)

    print(auth_url)

def get_access_token(code='123456789'):
    access_token_url = 'https://api.weibo.com/oauth2/access_token'
    import requests
    re_dict = requests.post(access_token_url, data={
        'client_id':'123456',
        'client_secret':'123456abc',
        'grant_type':'authorization_code',
        'code':code,
        'redirect_url':'http://127.0.0.1:8080/complete/weibo'
    })

def get_user_info(access_token='', uid=''):
    user_url = 'https://api.weibo.com/2/users/show.json?access_token={token}&uid={uid}'.format(token=access_token, uid=uid)

    print(user_url)

if __name__ == '__main__':
    #get_auth_url()
    #get_access_token(code='123456')

    get_user_info(access_token='123456test', uid='123456')