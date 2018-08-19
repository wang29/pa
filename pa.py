#!usr/bin/python
#coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
from lxml import etree


class MoocSelenium(unittest.TestCase):
    '''
    利用unittest模块的测试类来解决获取下一页的网页源码问题。
    正常情况，当点击下一页后，获取当前页的网页源码比较麻烦，而使用测试类的方法则可以很容易解决

    '''

    def setUp(self):
        '''
        初始化方法（固定写法）

        '''
        # 创建浏览器对象。
        self.driver = webdriver.Firefox()
        # 统计链接个数
        self.num = 0
        self.num2 = 1
        # 保存链接列表
        self.link_list = []
        # 请求网页,如果该行代码放在testMooc方法，会导致抓取的数据有重复，而且漏抓
        self.driver.get('https://www.icourse163.org/category/computer')

    def testMooc(self):
        while True:

            # 让网页完全加载，避免网页没加载完导致获取的数据丢失
            time.sleep(3)
            # 获取网页源码
            html = self.driver.page_source
            # 把源码解析为html dom文档
            content = etree.HTML(html)
            # 使用xpath去匹配所有的课程链接
            course_list = content.xpath('//div[@class="m-course-list"]//div[@class="u-clist f-bg f-cb f-pr j-href ga-click"]/@data-href')

            for item in course_list:
                # 拼接获取完整的课程链接
                link = 'https://www.icourse163.org' + item
                # 添加课程链接到保存的链接列表
                self.link_list.append(link)

            # 退出循环条件，从网页源码里面没找到某个类名，则返回为-1，进而作为当点击下一页时，如果没法点击时，则此时的返回值不为-1
            if (html.find('ux-pager_btn ux-pager_btn__next z-dis')) != -1:
                break

            # 模拟浏览器手动点击下一页
            self.driver.find_element_by_xpath('//li[@class="ux-pager_btn ux-pager_btn__next"]/a').click()

        # 输出课程链接及统计个数
        for each in self.link_list:
            if(self.num % 20 == 0):
                self.num2
                print('\n' + '='*30 + '第' + str(self.num2) + '页课程链接列表' + '='*30 + '\n')
                self.num2 += 1
            self.num += 1
            print(each)

        # 输出该学科的所有课程链接的个数
        print self.num,len(self.link_list)

    def tearDown(self):
        ''' 退出方法（固定写法）'''

        self.driver.quit()

if __name__ == '__main__':
    unittest.main()

