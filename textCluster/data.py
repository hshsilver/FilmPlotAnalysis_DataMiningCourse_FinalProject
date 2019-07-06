import json
import demjson
import urllib.request
import re
from lxml import etree
urllib.request.urlcleanup()
import urllib.error
import time

'''设置代理并将爬虫伪装成浏览器'''
def use_proxy(proxy_ip,url):
    try:
        req=urllib.request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0')
        proxy=urllib.request.ProxyHandler({'http':proxy_ip})
        opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        data=urllib.request.urlopen(req).read().decode('utf-8','ignore')
        return data
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
        time.sleep(10) #出现异常延时10s
    except Exception as e:
        print('exception:'+str(e))
        time.sleep(1)

'''爬取榜单上电影的链接'''
for i in range(0,250,25):
    url='https://movie.douban.com/top250?start='+str(i)
    proxy_ip='127.0.0.1:8888'
    data=use_proxy(proxy_ip,url)
    response = etree.HTML(data)
    link = response.xpath('//div[@class="pic"]/a/@href')

    for j in range(0,len(link)):
        thisurl=link[j]

        '''爬取剧情简介文本，并写入本地文件内容'''
        data=use_proxy(proxy_ip,thisurl)
        pat='<span property="v:summary".*?>(.*?)</span>'
        content=re.compile(pat,re.S).findall(data)
        pat1='<title>(.*?)</title>'
        title=re.compile(pat1,re.S).findall(data)
        content_data=content[0].replace('<br />','').strip().replace('\n','').replace(' ','')

        '''爬取剧情类型，并写入本地文件名称'''
        pat2 = '<span property="v:genre".*?>(.*?)</span>'
        kind = re.compile(pat2, re.S).findall(data)

        '''只爬取动作类的'''
        title = title[0].strip()
        title = title[0:(len(title)- 5)]
        title = ''.join(title)
        filename='D:/temp/data1/动作/'+str(title)+str(kind)+'.txt'

        flagflag = 0
        # kind = kind.split(',')
        for m in range(len(kind)):
            if (kind[m] == '动作'):
                flagflag = 1

        if flagflag==1:
            with open(filename,'w',encoding='utf-8') as fh:
                fh.write(content_data)

            flagflag = 0

        #doc = open('D:/temp/output/kind.txt', 'a')
        #print (str(title)+str(kind), file = doc)
        print(j) #确保程序在爬取

        '''所有种类都爬取'''
        '''title = title[0].strip()
        title = title[0:(len(title) - 5)]
        title = ''.join(title)
        filename = 'D:/temp/data2/' + str(title) + str(kind) + '.txt'

        with open(filename, 'w', encoding='utf-8') as fh:
            fh.write(content_data)

        doc = open('D:/temp/output/kind.txt', 'a')
        print(str(title) + str(kind), file=doc)
        print(j)'''


