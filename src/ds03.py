from urllib import urlopen
keyword='python'
resp = urlopen('https://www.google.com/search?q='+keyword)
html=resp.read()
len(html)
import re
p=re.compile('.*(error).*')
print p.search(html).group(1)
import webbrowser
webbrowser.open('http://www.google.com/search?q=python')
import urllib2
url = 'http://www.google.com/#q=python'
headers = {'User-Agent' : 'Mozilla 4.0'}
request = urllib2.Request(url, None, headers)
response = urllib2.urlopen(request)
print response.headers
html = response.read()
len(html)
import os
f=open(os.path.join('','mygoogle1.html'),'w')
f.write(html)
f.close()