import lxml.html
import requests

keyword='비오는'
r = requests.get("http://music.naver.com/search/search.nhn?query="+keyword+"&x=0&y=0")

_html = lxml.html.fromstring(r.text)
from lxml.cssselect import CSSSelector

sel = CSSSelector('table[summary] > tbody > ._tracklist_move > .name > a.title')
# Apply the selector to the DOM tree.
nodes = sel(_html)
for node in nodes:
    #print lxml.html.tostring(item)
    print node.text_content()