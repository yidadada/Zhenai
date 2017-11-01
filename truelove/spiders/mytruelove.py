# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
import json
import re
from truelove.items import TrueloveItem
from scrapy_redis.spiders import RedisSpider


class MytrueloveSpider(RedisSpider):
    name = 'mytruelove'
    allowed_domains = ['zhenai.com']
    #start_urls = ['http://search.zhenai.com/v2/search/pinterests.do?sex=1&agebegin=18&ageend=18&workcityprovince=-1&workcitycity=-1&h1=-1&h2=-1&salaryBegin=-1&salaryEnd=-1&occupation=-1&h=-1&c=-1&workcityprovince1=-1&workcitycity1=-1&constellation=-1&animals=-1&stock=-1&belief=-1&condition=66&orderby=hpf&hotIndex=0&online=']
    #redis_key = mytruelove:start_urls
    headers = {
        "Host": "search.zhenai.com",
        "Connection": "keep-alive",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        "Referer": "http://search.zhenai.com/v2/search/pinterest.do?sex=1&agebegin=18&ageend=18&workcityprovince=10102000&workcitycity=-1&h1=-1&h2=-1&salaryBegin=-1&salaryEnd=-1&occupation=-1&h=-1&c=-1&workcityprovince1=-1&workcitycity1=-1&constellation=-1&animals=-1&stock=-1&belief=-1&condition=66&orderby=hpf&hotIndex=0&online=",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
    }
    cookies = {
        "CHANNEL=^~refererHost=bzclk.baidu.com^~channelId=900122^~subid": "^~",
        " sid": "ClRqWFAuc8SRVmul0M7Y",
        " isSignOut": "%5E%7ElastLoginActionTime%3D1508482951672%5E%7E",
        " p": "%5E%7Eworkcity%3D10102005%5E%7Elh%3D108301207%5E%7Esex%3D1%5E%7Enickname%3D%E4%BC%9A%E5%91%98108301207%5E%7Emt%3D1%5E%7Eage%3D19%5E%7Edby%3D421bd6aa8786b3d8%5E%7E",
        " mid": "%5E%7Emid%3D108301207%5E%7E",
        " loginactiontime": "%5E%7Eloginactiontime%3D1508482951672%5E%7E",
        " logininfo": "%5E%7Elogininfo%3D%5E%7E",
        " hds": "2",
        " live800": "%5E%7EisOfflineCity%3Dtrue%5E%7EinfoValue%3DuserId%253D108301207%2526name%253D108301207%2526memo%253D%5E%7E",
        " bottomRemind": "%5E%7EvisPhoto%3Dno%5E%7E",
        " LOGIN_FIRST108301207": "%5E%7EmemberId%3D108301207%5E%7EendDate%3D2017%E5%B9%B410%E6%9C%8824%E6%97%A5%5E%7Elogincount%3D1%5E%7E",
        " REG_LOGIN": "%5E%7EnewUserFlag%3Dt%5E%7E",
        " __utma": "185049014.1611831390.1508482959.1508482959.1508482959.1",
        " __utmc": "185049014",
        " __utmz=185049014.1508482959.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd": "(none)",
        " JSESSIONID": "abcK4oNxqYmY17pobM48v",
        " Hm_lvt_2c8ad67df9e787ad29dbd54ee608f5d2": "1508482957",
        " Hm_lpvt_2c8ad67df9e787ad29dbd54ee608f5d2": "1508490365",
        " __xsptplusUT_14": "1",
        " __xsptplus14": "14.2.1508490054.1508490365.13%234%7C%7C%7C%7C%7C%23%23dt35rYa_IW0dPddf4Qy2kUoSqmx0v9mM%23",
    }

    def start_requests(self):
        start_urls = 'http://search.zhenai.com/v2/search/pinterests.do'
        yield scrapy.Request(url = start_urls,callback = self.parse_after,headers = self.headers,cookies = self.cookies)

    def parse_after(self, response):
        html =  response.body.decode('gbk')
        sex_list = ['1']
        age_list = range(18,100)
        province = {} #定义城市筛选项,使用字典是防止有数据重复
        with open('city.html', 'r') as f:
            html = etree.HTML(f.read())
            city_div = html.xpath('//div[@class="city_box"]')
            for city in city_div:
                city_id_list = city.xpath('.//a/@v')  #城市id,值
                province_id = city_id_list[0][:-2] + '00'  #省id,键
                province[str(province_id)] = city_id_list
                #print province
            for keys,values in province.items():
                pass

        base_url = 'http://search.zhenai.com/v2/search/getPinterestData.do?sex=%s&agebegin=%s&ageend=%s&workcityprovince=%s&workcitycity=%s&h1=-1&h2=-1&salaryBegin=-1&salaryEnd=-1&occupation=-1&h=-1&c=-1&workcityprovince1=-1&workcitycity1=-1&constellation=-1&animals=-1&stock=-1&belief=-1&condition=66&orderby=hpf&hotIndex=&online=&currentpage=%s&topSearch=false'
        for sex in sex_list:
            for age in age_list:
                for pro,cityid_list in province.items():
                    for city in cityid_list:
                        for page in range(1,101):
                            fullurl = base_url %(str(sex),str(age),str(age),str(pro),str(city),str(page))
                            yield scrapy.Request(url = fullurl,callback = self.parse_re,cookies = self.cookies,headers = self.headers)

    def parse_re(self,response):
        html =response.body
        a = re.findall(r'memberId":(\d+?),',html)
        for ever_id in a:
            #print ever_id
            detail_url='http://album.zhenai.com/u/%s' %ever_id
            #print detail_url
            yield scrapy.Request(url = detail_url,callback = self.parse_detail,cookies = self.cookies,headers = self.headers,priority=1)
        #priority 设置队列中的优先级

    def parse_detail(self,response):
        detail_list = response.xpath('//section[@class="mod-brief-info bgff radius-3 bord"]')
        for detail in detail_list:
            item = TrueloveItem()
            item['username']= detail.xpath('.//div[@class="brief-top p30"]/p/a[@class="name fs24"]/text()').extract()[0]
            item['userage'] = detail.xpath('.//div[@class="brief-center p20"]//tr[1]/td[1]/text()').extract()[0]
            item['userheight'] = detail.xpath('.//div[@class="brief-center p20"]//tr[1]/td[2]/text()').extract()[0]
            item['age'] = detail.xpath('.//div[@class="brief-center p20"]//tr[1]/td[1]/text()').extract()[0]
            item['usereducation']= detail.xpath('.//div[@class="brief-center p20"]//tr[2]/td[2]/text()').extract()[0]
            #print item['username'],item['userage'], item['usereducation']
            yield item














