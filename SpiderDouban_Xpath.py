#-*-coding:utf-8 -*-
'''
爬取豆瓣电影top250
'''
from lxml import etree
import time,requests,re,os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 写一个类
class Spider(object):
    def __init__(self):
        print u'开始爬取内容... ...'

    #拿到网页源代码
    def getHtml(self,url):
        html = requests.get(url)
        return html.text


    # 翻页操作
    def changPage(self,totalPage):
        urls = []
        for x in range(0,250,25):
            eachUrl = re.sub('start=(\d+)','start=%d'%x,url,re.S)
            urls.append(eachUrl)
        return urls
    # 获取网页源代码
    def getInfo(self,url):
        info = {}
        html = self.getHtml(url)#拿到网页源代码
        selector = etree.HTML(html)
        #总标题
        info['header_title'] = selector.xpath('//*[@id="content"]/h1/text()')[0]#豆瓣电影TOP250
        #25个电影名称
        info['titles'] = selector.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()')
        #是否可播放状态
        info['playbles']=[]
        for i in range(1,25+1):
            content = selector.xpath('//*[@id="content"]/div/div[1]/ol/li[%d]/div/div[2]/div[1]/span/text()' % i)
            info['playbles'].append(content)
        #导演演员人员信息
        info['man_info1'] = selector.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[1]')
        info['man_info2'] = selector.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[2]')
        #评分信息
        info['evalution_num'] = selector.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[@class="rating_num"]/text()')
        #参与评分人数
        info['evalutioners'] = selector.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[4]/text()')
        info['quote'] = selector.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[2]/span/text()')
        return info
    def saveInfo(self,eachUrl,info):
        num = int(re.search('start=(.*?)&filter',eachUrl,re.S).group(1))
        with open('DoubanMoviesTop250_xpath.txt','a') as f:
            for i in range(1,25+1):
                f.writelines('%s.'%(num+i) + info['titles'][i-1].replace('\n','') + '\n')

                try:
                    content = info['playbles'][i-1][0]
                    f.writelines(content.replace('\n','') + '\n')
                except:
                    f.writelines(u'[不可播放]'+'\n')

                f.writelines(info['man_info1'][i-1].replace(' ','').replace('\n','') + '\n')
                f.writelines(info['man_info2'][i-1].replace(' ','').replace('\n','') + '\n')
                f.writelines(info['evalution_num'][i-1].replace('\n','') + '\n')
                f.writelines(info['evalutioners'][i-1].replace('\n','') + '\n')
                f.writelines(info['quote'][i-1].replace('\n','') + '\n\n\n')

if __name__ == '__main__':
    doubanSpider = Spider()
    with open('DoubanMoviesTop250_xpath.txt','a') as f:
            f.writelines('***'+u'豆瓣电影TOP250'+'***\n\n\n')

    url = 'http://movie.douban.com/top250?start=0&filter='
    listUrl = doubanSpider.changPage(url)
    for eachUrl in listUrl:
        print u'正在爬取：' + eachUrl
        info = doubanSpider.getInfo(eachUrl)
        doubanSpider.saveInfo(eachUrl,info)
        time.sleep(5)
    print u'爬取完毕'