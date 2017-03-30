import urllib
uResponse = urllib.urlopen('http://python.org/')
_html = uResponse.read()
print len(_html)
import re
#p=re.compile('http://.+"')
p=re.compile('href="(http://.*?)"')
nodes=p.findall(_html)
print "how many http url?",len(nodes)
for i, node in enumerate(nodes):
    print i, node