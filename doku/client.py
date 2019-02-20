import xmlrpc.client

from doku.cookie_safe_transport import CookiesSafeTransport
from doku.cookie_transport import CookiesTransport


class Client:
    __proxy: xmlrpc.client.ServerProxy

    def __init__(self, domain, username, password, ssl=True, basepath='/'):
        transport = CookiesSafeTransport() if ssl else CookiesTransport()
        proto = 'https' if ssl else 'http'

        self.__proxy = xmlrpc.client.ServerProxy(
            '{proto}://{domain}{path}/lib/exe/xmlrpc.php'.format(
                proto=proto,
                domain=domain,
                path=basepath
            ),
            transport=transport
        )
        if not self.__proxy.dokuwiki.login(username, password):
            raise 'Login Failed'

    def call(self, method, *args):
        return getattr(self.__proxy, method)(*args)

