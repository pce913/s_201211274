#coding: utf-8
""" 트레이닝 데이터를 확보하기 위한 모듈.
    동아일보에서 연예관련 기사와 정치관련 기사의 개수를 수집함.
    정권비리를 덮으려 연예기사를 내는것이 사실인지 확인을 하기 위해서임.
    
    python [모듈이름] [키워드] [가져올 페이지 숫자] [큰 주제]
"""

import sys
from bs4 import BeautifulSoup
import urllib
import urllib2
import lxml.html
import requests
from lxml.cssselect import CSSSelector
#from urllib.parse import quote

ENTERTAINMENT_SUBJECT=['방송', '열애', '연예','가수', '배우', '아이돌' ,'멤버']
POLITICS_SUBJECT=['북한' ,'여당' ,'야당' ,'정치', '한미', '대통령', '정부']
BOUND_OF_SUBJECT={'방송':[33000,4830],'열애':[1500,300],'연예':[30000,3826],'가수':[9000,824],'배우':[15346,1867],
                 '아이돌':[1700,153],'멤버':[6100,750],
                 '북한':[9331,301],'여당':[2506,101],'야당':[4036,169],'정치':[39086,792],'한미':[3406,100],
                 '대통령':[29011,586],'정부':[27016,955]}

TARGET_URL_BEFORE_PAGE_NUM = "http://news.donga.com/search?"
TARGET_URL_BEFORE_KEWORD = '&query='
TARGET_URL_START_P='p='
TARGET_URL_REST = '&check_news=1&more=1&sorting=1&range=1&search_date='

CRITICAL_DATE=['2015-01-01','2015-01-19','2015-03-24','2015-03-24','2015-04-20','2015-07-01','2015-07-04','2015-07-24','2015-10-07']

#시작 페이지부터 몇 페이지를 가져와야 하나를 조사한다.


class Info:
    convert_date = 0
    entertainment=0
    politics=0


date_map=dict()
    
#key: 날짜 value: Info객체     init 필요 없다. 날짜가 들어오는데로 in키워드를 통해 key가 있는지 확인 해주면 된다.
  
output_file = open('result_articles.txt', 'w')

def get_news_date( URL, subject, big_subject):     #어떤 주제를 가진 기사가 어느 날짜에 쓰였는지를 가져오기.
    global output_file
    URL_with_page_num = URL
    r = requests.get( URL_with_page_num)
    _html = lxml.html.fromstring(r.text)
    sel = CSSSelector('#contents > div.searchContWrap > div.searchCont > div > div.t > p.tit > span')
    nodes = sel(_html)
    
    date=""
    for item in nodes:
        date=item.text_content().split()[0]            
        if date not in date_map:
             date_map[date]=Info()
        
        if big_subject=="entertainment":
            date_map[date].entertainment+=1
        else:
            date_map[date].politics+=1
        
    return len(nodes)



def main(argv):
    global output_file
    if len(argv) != 4:
        print("python [모듈이름] [키워드] [가져올 페이지 숫자] [큰 주제]")
        sys.exit(1)

    keyword = argv[1]
    page_num=int(argv[2])
    big_subject = argv[3]
    
    what_p = BOUND_OF_SUBJECT[keyword][0]
    for i in xrange(0,page_num):      #page_num 갯수만큼 페이지를 가져 온다는 뜻  약 70페이지를 가져와야 1000개 이상의 데이터를 확보 할 수 있음.
        target_URL = TARGET_URL_BEFORE_PAGE_NUM + TARGET_URL_START_P + str(what_p) +TARGET_URL_REST + TARGET_URL_BEFORE_KEWORD + urllib.quote(keyword) 
        what_p += get_news_date(target_URL,keyword,big_subject)
    
    print "one done"
    
if __name__ == '__main__':
    for subject in ENTERTAINMENT_SUBJECT:
        argv=['whatever',subject,BOUND_OF_SUBJECT[subject][1],'entertainment']
        main(argv)
    for subject in POLITICS_SUBJECT:
        argv=['whatever',subject,BOUND_OF_SUBJECT[subject][1],'politics']
        main(argv)
        
    for date in date_map.keys():
        result=""
        if(date in CRITICAL_DATE):
            result+="1"
        else:
            result+="0"
            
        result+=' '+date+' '+str(date_map[date].entertainment)+' '+str(date_map[date].politics)
        result+='\n'
        output_file.write(result)
    
    output_file.close()

    