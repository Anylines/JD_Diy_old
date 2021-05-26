import os, requests, re

def readCookie():
	if isv4:
		config = f'{env}/config/config.sh'
	else:
		config = f'{env}/config/cookie.sh' # 青龙
	with open(config, 'r', encoding='utf-8') as f:
		config = ''.join(f.readlines())
	cookies = re.findall(r"pt_key=.*;pt_pin=.*;", config)
	illegal_cookie = 'pt_key=xxxxxxxxxx;pt_pin=xxxx;'
	if illegal_cookie in cookies:
		m = cookies.index(illegal_cookie)
		del(cookies[m])
# 	for cookie in cookies: # 未完成
# 		TotalBean(cookie) # 未完成
	return cookies


def TotalBean(Cookie):
	url = "https://me-api.jd.com/user_new/info/GetJDUserInfoUnion"
	headers = {
		"Host": "me-api.jd.com",
		"Accept": "*/*",
		"Connection": "keep-alive",
		"Cookie": Cookie,
		"User-Agent": "jdapp;iPhone;9.4.4;14.3;network/4g;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1",
		"Accept-Language": "zh-cn",
		"Referer": "https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&",
		"Accept-Encoding": "gzip, deflate, br"
	}
	try:
		r = requests.get(url, headers= headers)
		if r.ok:
			res = r.json()
			if res['retcode'] == '1001':
				isLogin = False
				return isLogin
			if res['retcode'] == '0' and res['data'] and res['data']['userInfo']['baseInfo']:
				nickName = res['data']['userInfo']['baseInfo']['nickname']
			if res['retcode'] == '0' and res['data'] and res['data']['assetInfo']:
				beanCount = res['data']['assetInfo']['beanNum']
		else:
			print("京东服务器返回空数据")
	except Exception as e:
		print(e)
	return [nickName, beanCount]


if __name__ == '__main__':
	path_list = os.path.realpath(__file__).split('/')[1:]
	env = '/' + '/'.join(path_list[:-2]) # 容器外路径
	if os.path.isfile('/ql/config/cookie.sh') or os.path.isfile(f'{env}/config/cookie.sh'): # 青龙
		isv4 = False
		if not os.path.isfile(f'{env}/config/cookie.sh'): # 青龙容器内
			env = '/ql'
	else: # v4-bot
		isv4 = True
		if not os.path.isfile(f'{env}/config/config.sh'): # v4-bot 容器内
			env = '/jd'
	for cookie in readCookie():
		print(TotalBean(cookie))

    
