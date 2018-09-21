import hashlib
import re
import time
from PIL import Image
import pytesseract
import io
from gevent import monkey; monkey.patch_all()
import gevent

import requests
import random
import hmac
import hashlib
import binascii
import base64


class Auth(object):
    def __init__(self, appid, sid, skey):
        self._appid, self._secretid, self._secretkey = str(appid), str(sid), str(skey)

    def get_sign(self, bucket, howlong=86400):
        """ GET REUSABLE SIGN

        :param bucket: 图片处理所使用的 bucket
        :param howlong: 签名的有效时长，单位 秒

        :return: 签名字符串
        """

        if howlong <= 0:
            raise Exception('Param howlong must be great than 0')

        now = int(time.time())
        rdm = random.randint(0, 999999999)

        text = 'a=' + self._appid + '&b=' + bucket + '&k=' + self._secretid + '&e=' + str(
            now + howlong) + '&t=' + str(
            now) + '&r=' + str(rdm) + '&f='
        hexstring = hmac.new(self._secretkey.encode('utf-8'), text.encode('utf-8'), hashlib.sha1).hexdigest()
        binstring = binascii.unhexlify(hexstring)
        return base64.b64encode(binstring + text.encode('utf-8')).rstrip(), text

# ------------------------------
class ORC():
    def __init__(self):
        self.auth = Auth
        self.k = 'aDqYEC2iZIqHblnd9ZYTIxQirrkW8JLN'
        self.url = 'https://recognition.image.myqcloud.com/ocr/general'
        self.app_id = '1257651146'
        self.s_id = 'AKID66yjJkNJNMCwXwSOVYSClBva7Umc4F2f'
        self.s_key = 'aDqYEC2iZIqHblnd9ZYTIxQirrkW8JLN'
        self.save_name = None
        # self.url = 'http://recognition.image.myqcloud.com/ocr/general'


        self.headers = {
            "host": 'recognition.image.myqcloud.com',
            # "content-type": 'multipart/form-data',
            # "content-type": 'application/json',
            # "authorization": s,  # 鉴权签名
        }
        self.get_authorization()

    def get_authorization(self):
        a = self.auth(self.app_id, self.s_id, self.s_key)
        sign, text = a.get_sign('')
        self.headers["authorization"] = sign
        return sign

    def req_orc(self, img_byte):
        data = {
            "appid": self.app_id,
            # "bucket": 'test',
            "image": img_byte
        }
        return requests.post(self.url, files=data, headers=self.headers).json()

    def save_img_and_str(self, img_byte, data_json):
        """存储图片与识别结果"""
        try:
            save_name = self.save_name
            t = str(time.time())
            random.randint(0, 9)
            if not save_name:
                save_name = time.strftime("%y%m%d%H%M%S")
            file_name = "{}_{}{}".format(save_name, t[-2:], random.randint(0, 9))
            file_name = './ocr_img/' + file_name
            with open(file_name+'.png', 'wb')as f:
                f.write(img_byte)

            with open(file_name + '.txt', 'w')as f:
                f.write(str(data_json))
        except Exception as e:
            print("OCR"*10)
            print("save OCR error:", e)

    def get_img_str(self, img_byte):
        """对数据进行筛选
        特殊情况：
        1人 2018-09-05 汇缴201808
        """

        data_json = self.req_orc(img_byte)
        if 0 != data_json["code"]:
            print("ocr api error: ", data_json)

        self.save_img_and_str(img_byte, data_json)

        l = []
        l1 = []
        for i in data_json["data"]["items"]:
            s = i["itemstring"]
            s = s.replace(' ', '')
            date_list = re.findall(
                "^[^\u4E00-\u9FA5]*?(19[^\d]{0,1}\d[^\d]{0,1}\d[^\d]{0,1}[01]\d[^\d]{0,1}[0123]\d[^\u4E00-\u9FA5]{0,1}\d*|"
                "20[^\d]{0,1}\d[^\d]{0,1}\d[^\d]{0,1}[01]\d[^\d]{0,1}[0123]\d[^\u4E00-\u9FA5]{0,1}\d*)"
                "([\u4E00-\u9FA5]+\d{6}[-]*\d{6}|[\u4E00-\u9FA5]+\d{6}|[\u4E00-\u9FA5]+){0,}(.*)", s)
            if not date_list:
                l1.append(s)
                continue
            l.append(l1)
            l1 = [i for i in list(date_list[0]) if i != '']

        l.append(l1)
        return l

def ocr(img_byte, save_name=None):
    o = ORC()
    o.save_name = save_name
    return o.get_img_str(img_byte)


# -------------------------------
class ORC01():
    def __init__(self):
        self.str_list = []
        self.add_img_b = True
        self.to_black_b = True

    def byte_to_pil(self, byte):
        return Image.open(io.BytesIO(byte))

    def pil_to_byte(self, pil):
        img_byte = io.BytesIO()
        pil.save(img_byte, format='PNG')
        return img_byte.getvalue()

    def sub_str(self, s):
        s = s.replace('责〔', '汇')
        s = s.replace('′息', '息')
        s = s.replace('g', '8一')
        s = s.replace('O', '0')
        s = s.replace('霖〔', '汇')
        s = s.replace('墅敌', '缴')
        s = s.replace('〉', ',')
        return s


    def identify(self, pil, lang='chi_sim'):
        if isinstance(pil, bytes):
            pil = self.byte_to_pil(pil)
        if self.add_img_b:
            self.add_img(pil)
        if self.to_black_b:
            self.to_black(pil)
        s = pytesseract.image_to_string(pil)
        s = self.sub_str(s)
        self.str_list.append(s)
        return s

    def add_img(self, pil):
        x, y = pil.size
        for i, j in [(2, 16), (3, 16), (4, 16), (5, 16), (6, 16), (7, 16), (8, 16), (9, 16), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10), (10, 11), (10, 12), (10, 13), (10, 14), (10, 15), (10, 16), (11, 8), (11, 16), (12, 8), (12, 16), (13, 8), (13, 16), (14, 8), (14, 16), (15, 8), (15, 16), (16, 8), (16, 16), (17, 16), (20, 9), (21, 9), (22, 9), (23, 9), (24, 9), (25, 9), (26, 9), (27, 9), (28, 9), (29, 9), (30, 9), (31, 9), (32, 9), (33, 9), (34, 9), (36, 3), (37, 3), (37, 17), (38, 3), (38, 17), (39, 3), (39, 6), (39, 7), (39, 8), (39, 9), (39, 10), (39, 11), (39, 12), (39, 13), (39, 16), (39, 17), (40, 3), (40, 6), (40, 16), (41, 3), (41, 6), (41, 15), (41, 16), (42, 3), (42, 6), (42, 14), (42, 15), (43, 3), (43, 4), (43, 5), (43, 6), (43, 8), (43, 9), (43, 10), (43, 11), (43, 12), (43, 13), (43, 14), (44, 3), (44, 4), (44, 6), (44, 8), (44, 9), (44, 10), (44, 11), (44, 12), (44, 13), (44, 14), (45, 3), (45, 6), (45, 14), (46, 3), (46, 6), (46, 14), (46, 15), (47, 3), (47, 6), (47, 15), (48, 3), (48, 6), (48, 7), (48, 8), (48, 9), (48, 10), (48, 11), (48, 12), (48, 13), (48, 15), (48, 16), (49, 3), (49, 6), (49, 7), (49, 8), (49, 9), (49, 10), (49, 11), (49, 12), (49, 13), (49, 16), (50, 3), (50, 17), (51, 3), (51, 17)]:
            pil.putpixel((i+50, y-20-j), (0, 0, 0))
            pil.putpixel((x-50-i, y-20-j), (0, 0, 0))

    def to_black(self, pil):
        x, y = pil.size
        for i in range(x):
            for j in range(y):
                l = pil.getpixel((i, j))
                r, g, b = l[0], l[1], l[2]
                rgb = 180
                if r < rgb and g < rgb and b < rgb:
                    pil.putpixel((i, j), (0, 0, 0))
                else:
                    pil.putpixel((i, j), (255, 255, 255))


def ocr_old(byte_or_pil_list, add=True):
    o = ORC01()
    if add:
        o.add_img_b = add
    if not isinstance(byte_or_pil_list, list):
        byte_or_pil_list = [byte_or_pil_list]

    g_list = [gevent.spawn(o.identify, i) for i in byte_or_pil_list]
    for i in [g_list[i:i+3] for i in range(0, len(g_list), 3)]:
        gevent.joinall(i)
    return o.str_list




def cs():
    # 1:    17.7-19.7      17.7-19.0
    # 2:    20.2-24.1      10.1-12.0
    # 3:    20.0-29.9      06.7-10.0
    # 4:    23.7-30.7      05.9-07.5
    # 5:    32.8-40.7      06.6-08.0
    for i in range(1):
        tt = time.time()

        # pil = Image.open("sjz_gjj_img.png")
        pil = Image.open("3.png")
        # pil = pil.convert('1')
        x, y = pil.size
        # print(x, y)
        # print(pil.size)
        ll = []
        """
        for i in range(x):
            for j in range(y):
                l = pil.getpixel((i, j))
                r, g, b = l[0], l[1], l[2]
                # if 0 == i%200 and 100==j:
                # print((i, j), ">>>", pil.getpixel((i, j)))
                rgb = 180
                if r==g==b==0:
                    ll.append((i, j))
                if r < rgb and g < rgb and b < rgb:
                    pil.putpixel((i, j), (0, 0, 0))
                else:
                    pil.putpixel((i, j), (255, 255, 255))
        for i, j in [(2, 16), (3, 16), (4, 16), (5, 16), (6, 16), (7, 16), (8, 16), (9, 16), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10), (10, 11), (10, 12), (10, 13), (10, 14), (10, 15), (10, 16), (11, 8), (11, 16), (12, 8), (12, 16), (13, 8), (13, 16), (14, 8), (14, 16), (15, 8), (15, 16), (16, 8), (16, 16), (17, 16), (20, 9), (21, 9), (22, 9), (23, 9), (24, 9), (25, 9), (26, 9), (27, 9), (28, 9), (29, 9), (30, 9), (31, 9), (32, 9), (33, 9), (34, 9), (36, 3), (37, 3), (37, 17), (38, 3), (38, 17), (39, 3), (39, 6), (39, 7), (39, 8), (39, 9), (39, 10), (39, 11), (39, 12), (39, 13), (39, 16), (39, 17), (40, 3), (40, 6), (40, 16), (41, 3), (41, 6), (41, 15), (41, 16), (42, 3), (42, 6), (42, 14), (42, 15), (43, 3), (43, 4), (43, 5), (43, 6), (43, 8), (43, 9), (43, 10), (43, 11), (43, 12), (43, 13), (43, 14), (44, 3), (44, 4), (44, 6), (44, 8), (44, 9), (44, 10), (44, 11), (44, 12), (44, 13), (44, 14), (45, 3), (45, 6), (45, 14), (46, 3), (46, 6), (46, 14), (46, 15), (47, 3), (47, 6), (47, 15), (48, 3), (48, 6), (48, 7), (48, 8), (48, 9), (48, 10), (48, 11), (48, 12), (48, 13), (48, 15), (48, 16), (49, 3), (49, 6), (49, 7), (49, 8), (49, 9), (49, 10), (49, 11), (49, 12), (49, 13), (49, 16), (50, 3), (50, 17), (51, 3), (51, 17)]:
            pil.putpixel((i+50, y-20-j), (0, 0, 0))
            pil.putpixel((x-50-i, y-20-j), (0, 0, 0))
        # for i in range(40):
        #     for j in [0,1, 10,11, 22,23]:
        #         pil.putpixel((50+i, y-20-j), (0, 0, 0))
        #         pil.putpixel((x-50-i, y-20-j), (0, 0, 0))
        pil.show()
        print(ll)
        # input("继续")
                """

        pil_list = [pil] * 1
        for i in ocr(pil_list):
            print("---")
            print(i)

        print(time.time()-tt)
        print()

def t():
    from PIL import Image

    img = Image.open("result.png")
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            try:
                print(img.getpixel((i, j)))
                # r, g, b, alpha = img.getpixel((i, j))
                r, g, b = img.getpixel((i, j))

                print(r, g, b)
                """
                if r == 0 and g == 0 and b == 0:
                    # g = 204
                    # img.putpixel((i, j), (255, 255, 255, alpha))
                    img.putpixel((i, j), (255, 255, 255))
                else:
                    # img.putpixel((i, j), (0, 0, 0, alpha))
                    img.putpixel((i, j), (0, 0, 0))
                """

            except Exception as e:
                # print(i, j)
                continue
    img.show()

if __name__ == '__main__':
    # cs()
    from hashlib import sha1
    import hmac
    import base64

    k = 'AKID66yjJkNJNMCwXwSOVYSClBva7Umc4F2f'
    s = 'a=1257651146b=k=AKID66yjJkNJNMCwXwSOVYSClBva7Umc4F2fe=7776000t=%sr=846521365r=' % (str(int(time.time())))

    my_sign = hmac.new(k.encode("utf-8"), s.encode("utf-8"), sha1).digest()
    # print(my_sign)
    my_sign = base64.b64encode(my_sign)
    print(my_sign)
    print(s)


    from hashlib import sha1
    import hmac
    import base64
    k = 'AKID66yjJkNJNMCwXwSOVYSClBva7Umc4F2f'


    s = 'a=APPID&k=YOaUR SECRET_ID&e=1537338779&t=1537252379&r=34338878030&f='
    k = 'YOUR SECRET_KEY'


    my_sign = hmac.new(k.encode("utf-8"), s.encode("utf-8"), sha1).digest()
    # print(my_sign)
    my_sign = base64.b64encode(my_sign)
    print(my_sign)

    print('\n')
    string_b = bytes(s, encoding="utf-8")
    key_b = bytes(k, encoding="utf-8")
    signature = base64.b64encode(hmac.new(key=key_b, msg=string_b, digestmod=hashlib.sha256).digest())
    print(signature.decode("utf-8"))

    # UN8U8kzQ2kS6Xc+AWxOncc1ilk5hPUFQUElEJms9WU9hVVIgU0VDUkVUX0lEJmU9MTUzNzMzODc3OSZ0PTE1MzcyNTIzNzkmcj0zNDMzODg3ODAzMCZmPQ==



    """
    from PIL import Image
    img = Image.open("result.png")
    print(img.size)
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            print(i, j)
            try:
                # print(img.getpixel((i, j)))
                # r, g, b, alpha = img.getpixel((i, j))
                r, g, b = img.getpixel((i, j))
                def zzz(x, y):
                    r, g, b = img.getpixel((x, y))
                    if r==g==b==255:
                        return 1
                    a=0;b=0;c=0;d=0
                    if x<i+1:
                        a = zzz(x+1, y)
                    if y<j+1:
                        b = zzz(x, y+1)
                    if x>i-1:
                        c = zzz(x-1, y)
                    if y>j-1:
                        d = zzz(x, y-1)

                    if a==b==d==c==1:
                        return 4


                if r==g==b==0:
                    if 4 == zzz(i, j):
                        for a in range(i-1, i+1):
                            for b in range(j-1, j+1):
                                img.putpixel((a, b), (255, 255, 255))


                # print(r, g, b)
                if r == 0 and g == 0 and b == 0:
                    # g = 204
                    # img.putpixel((i, j), (255, 255, 255, alpha))
                    img.putpixel((i, j), (255, 255, 255))
                else:
                    # img.putpixel((i, j), (0, 0, 0, alpha))
                    img.putpixel((i, j), (0, 0, 0))

            except Exception as e:
                # print(i, j)
                continue
    img.show()
    # img.save("333.png")
    """




    """
    from PIL import Image
    image_file = Image.open("timg1.jpg") # open colour image
    image_file = image_file.convert('1') # convert image to black and white
    image_file.save('result.png')
    """
