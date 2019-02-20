from xmlrpc.client import Transport


class CookiesTransport(Transport):
    """A Python3 xmlrpc.client.Transport subclass that retains cookies."""
    def __init__(self):
        super().__init__()
        self._cookies = dict()

    def send_headers(self, connection, headers):
        if self._cookies:
            cookies = map(lambda x: '='.join(x), self._cookies.items())
            connection.putheader("Cookie", "; ".join(cookies))
        super().send_headers(connection, headers)

    def parse_response(self, response):
        """parse and store cookie"""
        try:
            for header in response.msg.get_all("Set-Cookie"):
                cookie = header.split(";", 1)[0]
                cookieKey, cookieValue = cookie.split("=", 1)
                self._cookies[cookieKey] = cookieValue
        finally:
            return super().parse_response(response)

