# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import urllib.request as urllib2
import os

import _thread

from image_spider.data.DemoDB import DemoDB

img_list_db = DemoDB("img_list.slqite3.db",False)

root_dir = "d:\\nushens\\"

def mkdir(path):


 
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
 
        #print (path,' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        #print (path,' 目录已存在')
        return False

def getDirNameFromName(name):
    import re
    dn = root_dir + ''.join(re.findall('[\u4e00-\u9fa5]',name))
    print("目录为：",dn)
    return dn
def getFileNameFromAddr(addr):
    fn = addr.replace("/","I").replace(":","_").replace(":","_")
    return fn;

def IsExist(filename):
  
    root = root_dir

    for dirpath, dirnames, filenames in os.walk(root):
        for filepath in filenames:
            if filename == filepath :
                return True
   
    return False

def thread_download_img(item):

    dirName = getDirNameFromName(item["name"])
    fileName = getFileNameFromAddr(item["addr"])

    print("begin to download in path: ",dirName,fileName)

    #return 0

    if img_list_db.query(item['addr']):
        print("already downloaded:",item['addr'],item['name'])
        return True
    else:
        mkdir(dirName)
        file_name = os.path.join(dirName,fileName)

        print("realPath:",file_name)


        if not os.path.exists(file_name) and not IsExist(item['name']+'.jpg'):
            print ("get  " , item['addr'] ,"=>",file_name)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
            req = urllib2.Request(url=item['addr'],headers=headers)
            
            try:
                res = urllib2.urlopen(req,timeout=10)
                
                with open(file_name,'wb') as fp:
                    fp.write(res.read())
                print("geted:",item['addr'],file_name)  
            except :
                print("get error ")
                return False
        else:
              print("exist:",item['addr'],file_name)  

        img_list_db.insert(item['addr'],file_name)
        return True

class ImageSpiderPipeline:
    def process_item(self, item, spider):
        thread_download_img(item)
        return item
