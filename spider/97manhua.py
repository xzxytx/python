# -*- utf-8 -*-
# 名称：       漫画 url: https://www.97manhua.com
# 创建时间：     2018/08/04
# 修改时间：     2018/08/04
import re
import os
import requests
import time

HEADERS = {
    # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'Accept-Encoding':'gzip, deflate',
    # 'Accept-Language':'zh-CN,zh;q=0.9',
    # 'Cache-Control':'no-cache',
    # 'Connection':'keep-alive',
    # 'Host':'mhpic.mh51.com',
    # 'Pragma':'no-cache',
    # 'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
}
# SESS = requests.session()
# SESS.headers.update(HEADERS)
SESS = requests

class Comic(object):
    def __init__(self):
        self.sess = SESS
        self.error_url_list = []
        self.comic_name = '漫画'
        self.path = './'

    def save_img(self, file_name, content):
        """
        接受二进制文件，与文件名 进行存储到本地
        :param file_name: 路径 + 文件名
        :param content: 二进制流
        :return: None
        """
        if -1 == file_name.find('/'):
            file_name = '{}{}/{}'.format(self.path, self.comic_name, file_name)
        dirs = re.findall('.*/', file_name)[0]
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        with open(file_name, "wb")as f:
            f.write(content)
        return 1

    def req_img(self, url, req_type="GET"):
        """
        请求网址
        :param url:网址
        :req_type;get, post
        :return: response
        """
        if 'get' == req_type.lower():
            return self.sess.get(url)

    def judge_response_type(self, response):
        """
        根据返回headers来判断 的是否为图片类型
        :param response: response
        :return: 1:是， 0:不是
        """
        if 'image' in response.headers["Content-Type"]:
            return 1

    def extract_url_file_name(self, url):
        """
        提取网址中的一部分为文件名
        :param url: 网址
        :return: 文件名
        """
        file_name_list = re.findall('.*?\.jpg', url)
        if not file_name_list:
            return
        file_name = file_name_list[-1][-20:]
        file_name = file_name.replace('/', '_')
        file_name = re.findall("\d.*", file_name)[0]

        return file_name


    def save_url_list(self, url_list):
        """
        请求图片网址并存储
        :param url_list: type:list, ["www...", "www..."]
        :return: type:list,  返回失败网址
        """
        if not url_list:
            return self.error_url_list
        url = url_list.pop()
        file_name = self.extract_url_file_name(url)
        response = self.req_img(url)
        if not self.judge_response_type(response) or not file_name:
            self.error_url_list.append(url)
        else:
            self.save_img(file_name, response.content)

        return self.save_url_list(url_list)


class ManHua97(Comic):

    def __init__(self, comic_name="漫画名"):
        super(ManHua97, self).__init__()
        self.comic_name = comic_name
        self.base_url = 'https://www.97manhua.com'
        self.n = 0
        self.error_number = 0

    def req_page(self, url):
        """
        请求漫画页面
        :return:
        """
        return self.sess.get(url)

    def extract_img_url(self, response):
        """
        提取图片url， 与下一张的url
        :param response:
        :return:图片网址list， 下一张网址  例：['www...', 'www..'], 'www.'
        """

        try:
            # 提取下一张页面
            next_page_str = re.findall('chapterTree=\[([^\]]+)', response.text)[0]
            next_page_list = re.findall('\d+', next_page_str)
            next_url = ''
            if len(next_page_str) >= 2:
                next_url = next_page_list[-1]

            # 提取图片url
            more_url_str = re.findall('picTree\s*=\s*\[([^\]]+)', response.text)[0]
            img_url_list = re.findall("""['"]([^'"]+)['"]""", more_url_str)[:-1]
        except Exception as e:
            print('response.text:', response.text)
            raise e

        return img_url_list, next_url

    def start(self, page='1100373', t=4):
        """
        执行方法
        :param page: 网址的起始数字
        :param t: 每页延时
        :return: 没成功的网址 list
        """
        self.n += 1
        self.error_number += 1
        if not page or '0' == page or self.error_number>4:
            print("失败：", self.error_url_list)
            return self.error_url_list
        url = '{}/chapter/{}.shtml'.format(self.base_url, page)
        print(url, self.n)
        try:
            response = self.req_page(url)
            img_url_list, url = self.extract_img_url(response)
            self.save_url_list(img_url_list[::-1])
            self.error_number = 0
        except Exception as e:
            print(e)

        time.sleep(t)
        return self.start(url)

def main(name, page):
    t = time.time()
    d = ManHua97(name)
    try:
        d.start(page=page)
    except Exception as e:
        print("错误网址：", d.error_url_list)
        raise e
    print("用时：", time.time() - t)

if __name__ == '__main__':
    main(name="绝世唐门", page="1100848")
    
    # 错误再次下载
    # url_list = ['http://mhpic.mh51.com/comic/Y/妖神记/178话上/10.jpg-smh.middle', 'http://mhpic.mh51.com/comic/Y/妖神记/178话上/11.jpg-smh.middle', 'http://mhpic.mh51.com/comic/Y/妖神记/178话上/12.jpg-smh.middle', 'http://mhpic.mh51.com/comic/Y/妖神记/178话上/13.jpg-smh.middle', 'http://mhpic.mh51.com/comic/Y/妖神记/178话上/14.jpg-smh.middle', 'http://mhpic.mh51.com/comic/Y/妖神记/178话上/15.jpg-smh.middle']
    # d = ManHua97()
    # a = d.save_url_list(url_list)
    # for i in a:
    #     print(i)
