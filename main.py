import requests
from lxml import etree

import os
import time

import conf


def getHtml(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    return resp.text


def parseChapterURL(html):
    root = etree.HTML(html)
    title = root.xpath('//*[(@id = "list")]//a/text()')
    # print(title)
    chapterUrlList = root.xpath('//*[(@id = "list")]//a/@href')
    print('title:', len(title))
    print('url:', len(chapterUrlList))    
    result = []
    for i in zip(title, chapterUrlList):
        # 判断是否为章节链接：使用正则表达式
        if i[0].startswith('第'):
            result.append(i)
        # result.append(i)
    return result


def parseChapterContent(html):
    root = etree.HTML(html)
    content = []
    title = ''.join(root.xpath('//*[(@id = "neirongDiv")]//h1/text()')).strip()
    content.append(title)
    paragraph = root.xpath('//*[(@id = "zjneirong")]/p/text()') if root.xpath('//*[(@id = "zjneirong")]/p/text()') else root.xpath('//*[(@id = "zjneirong")]/text()') 
    for text in paragraph:
        content.append(text.strip())
    return (os.linesep * 2).join(content)


def saveTxt(content, fileName=conf.FILE_NAME, mode='a', encoding='utf-8'):
    with open(file=fileName, mode=mode, encoding=encoding) as fw:
        fw.write(content)
        fw.write(os.linesep*2)


def test():
    # print(parseChapterURL(getHtml(conf.TXT_URL)))
    # print(parseChapterContent(getHtml(conf.CHAPTER_TEST_URL)))
    chapterUrlList =parseChapterURL(getHtml(conf.TXT_URL))
    print(len(chapterUrlList))
    for url in chapterUrlList:
        content = parseChapterContent(getHtml(url[1]))
        saveTxt(content)
        print(url[0], '下载完成')
        time.sleep(1)
    print('全部下载完成')
    


def main():
    test()


if __name__ == '__main__':
    main()
