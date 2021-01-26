import scrapy

from image_spider.data.DemoDB import DemoDB 

from image_spider.PicItem import PicItem


class Www26abcComSpider(scrapy.Spider):
    name = 'www26abc'
    allowed_domains = ['www.26abc.com']
    # 初始URL
   # start_urls = ['https://www.zbjuran.com/mei/']
   # scrapy crawl xh --nolog
    start_urls = ['https://www.26abc.com/tupian/ent/meinvtupian/30188_3.html']
    # 设置一个空集合
    #url_set = set()

    url_list_db = DemoDB("url_list.slqite3.db",False)

    def parse(self, response):
        
        if (False == Www26abcComSpider.url_list_db.query(response.url,1)):

            Www26abcComSpider.url_list_db.update(response.url)

            #print ("2.get img ing ...... ",sys._getframe().f_lineno)

            if True :
                #or response.url.startswith("https://www.nvshens.org/g/32336/"):
                
                
                allPics = response.xpath('//div[@id="picBody"]/p/strong/a/img')

                print ("34 .....   2.get img ing ...... ",allPics)
                for pic in allPics:
                    # 分别处理每个图片，取出名称及地址
                    #print ("2.get img ing ...... ",sys._getframe().f_lineno )
                    item = PicItem()
                    #print ("2.get img ing ...... ",sys._getframe().f_lineno )
                    addr =  pic.xpath('@src').extract()[0]

                    name = pic.xpath('@alt').extract()[0]
                    
                    item['name'] = name.replace('/','_').replace(':','_').replace('[','_').replace(']','_').replace(' ','_')
                        

                    item['addr'] = addr
                    # 返回爬取到的信息
                    print ("hav:",item['addr'],item['name'])
                    #print ("2.get img ing ...... ",sys._getframe().f_lineno )
                    yield item
                print ("2.get img ing ...... 50")
            # 获取所有的地址链接
            #print ("2.get href ing ...... ")
            urls= response.xpath("//a/@href").extract()
        
            for url in urls:
                #print(url)
                url_arr = url.split("_")
                # 如果地址以http://www.xiaohuar.com/list-开头且不在集合中，则获取其信息
                if url.startswith("/tupian/") :
                    #and url.endswith(".html"):
                    
                    url_whole = "https://www.26abc.com/"+url

                    if Www26abcComSpider.url_list_db.query(url_whole):
                        #print ("Exist:",url,url_whole)
                        pass
                        
                    else:
                        #XhSpider.url_set.add(url_whole)
                        Www26abcComSpider.url_list_db.insert(url_whole)
                        # 回调函数默认为parse,也可以通过from scrapy.http import Request来指定回调函数
                        # from scrapy.http import Request
                        # Request(url,callback=self.parse)
                        print ("add",url_whole)
                        yield self.make_requests_from_url(url_whole)
                
                elif url.startswith("http") and url.endswith(".html"):
                    
                    url_whole = url

                    if Www26abcComSpider.url_list_db.query(url_whole):
                        #print ("Exist:",url,url_whole)
                        pass
                    else:
                        #XhSpider.url_set.add(url_whole)
                        Www26abcComSpider.url_list_db.insert(url_whole)
                        # 回调函数默认为parse,也可以通过from scrapy.http import Request来指定回调函数
                        # from scrapy.http import Request
                        # Request(url,callback=self.parse)
                        print ("add",url_whole)
                        yield self.make_requests_from_url(url_whole)
                else:             

                    pass
        
        
        print ("3.get waiting href ... ")

        url_whole =  Www26abcComSpider.url_list_db.query_data()

        if len(url_whole) > 10:
            yield self.make_requests_from_url(url_whole)
        else:
            print ("4. we finished this site")


