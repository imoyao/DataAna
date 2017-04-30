#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import re
import sys

import urllib2
from lxml import etree

reload(sys)
sys.setdefaultencoding("utf-8")

url = 'http://www.snchangwu.gov.cn/zjzw/xzgk.htm'

def get_html(url):  #
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    headers = {'User-Agent': user_agent} 
    req = urllib2.Request(url, headers = headers)
    response = urllib2.urlopen(req)
    html = response.read()
    return html

def get_target_url(pre_html):
    html = etree.HTML(pre_html)
    names = html.xpath('//div[@class = "newsrcon fr"]/ul/li/a/text()')
    urls = html.xpath('//div[@class = "newsrcon fr"]/ul/li/a/@href') 
    target_urls = ["http://www.snchangwu.gov.cn" + i[2:len(i)] for i in urls]
    info_dict =dict(zip(names,target_urls))
    target_info = json.dumps(info_dict).decode("unicode-escape").encode("utf-8")    #str

    write_file("info.json",target_info)
    return target_urls


def get_real_data_file(ret_html):
    html_Element = etree.HTML(ret_html)
    html_title = get_title(html_Element)
    # print type(html_title)
    #前端好坑
    content_list = html_Element.xpath('//div[@id=\"vsb_newscontent\"]/text()') or html_Element.xpath('//div[@id=\"vsb_newscontent\"]/p/text()')
    content = "\n".join(content_list).encode("utf-8")
    # print type(content)
    w_file_name = html_title+".txt"
    write_file(w_file_name,content)
    return content

def re_file(info_str):
    # print type(info_str)
    family_num = re.search( r'(\d+户)', info_str, re.M|re.I).group().decode("utf-8")
    people_num = re.search( r'(\d+人|\d+万人|\d+\.\d+万人)', info_str, re.M|re.I).group().decode("utf-8")
    total_area = re.search( r'(\d+平方公里|\d+\.\d+平方公里)', info_str, re.M|re.I).group().decode("utf-8")
    # print type(family_num)
    return family_num,people_num,total_area


def get_title(html_Element):
    html_title = html_Element.xpath('//title/text()')[0][:-8]
    return html_title.encode("utf-8")

def write_file(w_file_name,content):
    with open(w_file_name,"w") as f:
        f.write(content)
    print "{} write finished.".format(w_file_name)

def read_file(r_file_name):
    with open(r_file_name,"r") as f:
        data_info = f.read()
    print "read {} finished.".format(r_file_name)
    return data_info


def main():
    global url
    pre_html = get_html(url)
    # print pre_html
    target_urls = get_target_url(pre_html)
    for url_item in target_urls:
        print "this is url:",url_item
        ret_html = get_html(url_item)
        time.sleep(2)
        info_str = get_real_data_file(ret_html)
        got_info = re_file(info_str)
        with open("detail.txt","a+") as f:
            f.write(str(got_info)+"\n")
    print "打开看看吧..."
    #文件最后存json


if __name__ == '__main__':
    main()

