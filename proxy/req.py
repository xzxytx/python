import requests


class GetProxy(object):
    """proxy"""
    @staticmethod
    def _get_proxy():
        # 代理服务器
        proxyHost = "http-pro.abuyun.com"
        proxyPort = "9010"

        # 代理隧道验证信息
        proxyUser = "zhou"
        proxyPass = "yu"

        proxyMeta_https = "https://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }

        proxyMeta_http = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }

        proxy = {
            'http': proxyMeta_http,
            'https': proxyMeta_https
        }
        return proxy


class RequestBase(GetProxy):
    """request base"""
    def __init__(self, req=None):
        self.req = req
        if not self.req:
            self.req = requests

        self.proxy = self._get_proxy()

    def get(self, url, params=None, **kwargs):
        print(**kwargs)
        return self.req.get(url, params=params, **kwargs, proxies=self.proxy)

    def post(self, url, data=None, json=None, **kwargs):
        print(url, data, json, **kwargs)
        return self.req.post(url, data=data, json=json, **kwargs, proxies=self.proxy)


class NormalRequest(RequestBase):
    """normal request"""
    pass


class SessionRequest(RequestBase):
    """requests session()"""
    def __init__(self, sess, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        RequestBase.__init__(self, *args, **kwargs)
        self.sess = sess
        self.req = self.sess

        self.headers = self.sess.headers
        self.cookies = self.sess.cookies


def get_proxy():
    return GetProxy()._get_proxy()


def session():
    s = requests.session()
    s.headers.update()
    return SessionRequest(s)


def get(*args, **kwargs):
    return NormalRequest().get(*args, **kwargs)


def post(*args, **kwargs):
    return NormalRequest().get(*args, **kwargs)


if __name__ == '__main__':
    pass


