'''
:method	POST
:path	/app/drug/details?mc_sign=b4759ed9816aad597eadf469da709472867bb157&timestamp=1553139656417
:authority	newdrugs.dxy.cn
:scheme	https
accept	application/json; charset=utf-8
user-agent	dxyapp_name/drugs dxyapp_ac/4124c5f1-1029-4fda-b06f-a87ac5ad8d11 dxyapp_version/9.3.1 dxyapp_system_version/5.1.1 dxyapp_client_id/000000004a8d42a5ffffffffa286b074 dxyapp_sid/bfa328f68df544c9907ef1df73c39eff dxyapp_ac/4124c5f1-1029-4fda-b06f-a87ac5ad8d11
app-os	5.1.1
app-version	9.3.1
app-mc	000000004a8d42a5ffffffffa286b074
app-ac	4124c5f1-1029-4fda-b06f-a87ac5ad8d11
app-hard-name	OPPO+R11
app-session-id	bfa328f68df544c9907ef1df73c39eff
app-v-user	dxy_n1sh6ip4
dxy-auth-token	TGT-973-06FFxIsPfyaNzacTJoTsPTxNAPYQ69uMqkQ-50
referer	https://newdrugs.dxy.cn
app-mt	OPPO%2BR11
content-type	application/json; charset=utf-8
content-length	42
accept-encoding	gzip
'''

'''
:method: POST
:path: /app/drug/details?mc_sign=bcad4bba58708341612bf9cbb0a077f6f1b1bc3e&timestamp=1553139861744
:authority: newdrugs.dxy.cn
:scheme: https
accept: application/json; charset=utf-8
user-agent: dxyapp_name/drugs dxyapp_ac/4124c5f1-1029-4fda-b06f-a87ac5ad8d11 dxyapp_version/9.3.1 dxyapp_system_version/5.1.1 dxyapp_client_id/000000004a8d42a5ffffffffa286b074 dxyapp_sid/bfa328f68df544c9907ef1df73c39eff dxyapp_ac/4124c5f1-1029-4fda-b06f-a87ac5ad8d11
app-os: 5.1.1
app-version: 9.3.1
app-mc: 000000004a8d42a5ffffffffa286b074
app-ac: 4124c5f1-1029-4fda-b06f-a87ac5ad8d11
app-hard-name: OPPO+R11
app-session-id: bfa328f68df544c9907ef1df73c39eff
app-v-user: dxy_n1sh6ip4
dxy-auth-token: TGT-973-06FFxIsPfyaNzacTJoTsPTxNAPYQ69uMqkQ-50
referer: https://newdrugs.dxy.cn
app-mt: OPPO%2BR11
content-type: application/json; charset=utf-8
content-length: 43
accept-encoding: gzip
'''

import requests
from requests.packages import urllib3

header = {
    'accept': 'application/json; charset=utf-8',
    'app-os': '5.1.1',
    'app-version': '9.3.1',
    'app-mc': '000000004a8d42a5ffffffffa286b074',
    'app-ac': '4124c5f1-1029-4fda-b06f-a87ac5ad8d11',
    'app-hard-name': 'OPPO+R11',
    'app-session-id': 'bfa328f68df544c9907ef1df73c39eff',
    'app-v-user': 'dxy_n1sh6ip4',
    'dxy-auth-token': 'TGT-973-06FFxIsPfyaNzacTJoTsPTxNAPYQ69uMqkQ-50',
    'referer': 'https://newdrugs.dxy.cn',
    'app-mt': 'OPPO%2BR11',
    'content-type': 'application/json;charset=utf-8',
    'accept-encoding': 'gzip',
    'protocol': 'HTTP/2.0',
    'user-agent': 'dxyapp_name/drugs dxyapp_ac/4124c5f1-1029-4fda-b06f-a87ac5ad8d11 dxyapp_version/9.3.1 dxyapp_system_version/5.1.1 dxyapp_client_id/000000004a8d42a5ffffffffa286b074 dxyapp_sid/bfa328f68df544c9907ef1df73c39eff dxyapp_ac/4124c5f1-1029-4fda-b06f-a87ac5ad8d11'
}
header1 = {
    'Content-Type': 'application/json;charset=utf-8'
}

url = 'https://newdrugs.dxy.cn/app/drug/details?mc_sign=55ba3e7f746171cde4cd8c5771e21896078374b6&timestamp=1553150588934'
hc_url = 'https://drugs.dxy.cn/user/api/v1.0/drug/medicareAndprice?drugId=123009&u=dxy_n1sh6ip4&s_sid=bfa328f68df544c9907ef1df73c39eff&username=dxy_n1sh6ip4&vs=5.1.1&mc=000000004a8d42a5ffffffffa286b074&hardName=OPPO%20R11&bv=2013&ac=4124c5f1-1029-4fda-b06f-a87ac5ad8d11&deviceName=OPPO%252BR11&mc_sign=a05a8c3121f33ddf3745de5df93104d6e6746b02&vc=9.3.1'
dt = {'id': '127247', 'category': '2', 'vsNames': ''}
urllib3.disable_warnings()
html = requests.post(url=url, headers=header, data=dt, verify=False)
# html=requests.get(url=hc_url,headers=header,verify=False)
print(html.status_code)
print(html.text)
