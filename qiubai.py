# -*- coding: utf-8 -*-
__author__ = 'Hao'

import urllib
import urllib2
import re


# 糗事百科爬虫类
class QS:
    # 初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56'
        self.headers = {'USER-AGENT': self.user_agent}
        # 存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        # 存放程序是否继续运行的变量
        self.enable = False

    def getPage(self, pageIndex):
        try:
            url = "http://www.qiushibaike.com/hot/page/" + str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8', 'ignore')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接糗事百科失败，错误原因", e.reason
                return None

    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败...."
            return None

        pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?' +
                             'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',
                             re.S)
        items = re.findall(pattern, pageCode)
        # 用来存储每一页的段子们
        pageStories = []

        for item in items:
            haveImg = re.search("img", item[3])
            if not haveImg:
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR, "\n", item[1])
                pageStories.append([item[0].strip(), text.strip(), item[2].strip(), item[4].strip()])
        return pageStories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    def getOneStory(self, pageStories, page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t页面ID:%s\t赞:%s\n%s" % (page, story[0], story[2], story[3], story[1])

    # 开始方法
    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，Q退出"
        self.enable = True
        self.loadPage()
        self.loadPage()
        # 局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                # 从全局list中获取一页的段子
                pageStories = self.stories[0]
                # 当前读到的页数加一
                nowPage += 1
                # 将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 输出该页的段子
                self.getOneStory(pageStories, nowPage)


spider = QS()
spider.start()
