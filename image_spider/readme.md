
# 项目介绍
项目以从图片网站获取图片为示范。使用图片的alt（汉字）创建目录，将图片url作为文件名（去掉:/等符号）。

```cmd
scrapy startproject image_spider
```

# 分析页面结构
爬虫需要明确哪些是内容，哪些是索引。索引要纳入遍历。内容要获取并存储。
1. 索引页面
   
   ![list](http://wp.my-soft.net.cn/wp-content/uploads/2021/01/nvshens.list_-1-1024x391.png "index")
   

2. 内容页面

   ![content](http://wp.my-soft.net.cn/wp-content/uploads/2021/01/nvshens.content-1024x330.png "index")
# 编写爬虫
```cmd
scrapy startproject image_spider
```

# 运行
```bash
scrapy crawl image_spider
```