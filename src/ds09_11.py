import os
import src.mylib
SERVICE='ArpltnInforInqireSvc'
OPERATION_NAME='getMinuDustFrcstDspth'
params1=os.path.join(SERVICE,OPERATION_NAME)
print params1
import urllib

keyPath=os.path.join(os.getcwd(), 'src', 'key_properties')
key=src.mylib.getKey(keyPath)

_d=dict()
#_d['stationName']='종로구'
_d['dataTerm']='month'
params2 = urllib.urlencode(_d)
print params2
params=params1+'?'+'serviceKey='+key['gokr']+'&'+params2
#print params
import urlparse
_url='http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc'
url=urlparse.urljoin(_url,params)
url=url.replace('\\','/')
print url
import requests

data=requests.get(url).text
print data