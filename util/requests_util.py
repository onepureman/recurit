import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Requests:
    """
    二次封装 requests 请求
    """

    @staticmethod
    def get(
            url: str, headers: dict = {}, cookies: dict = None, timeout: int = 10, verify: bool = False,
            proxies: dict = None, params: dict = None,
            ):

        res = requests.get(url, headers=headers, cookies=cookies, verify=verify, proxies=proxies, timeout=timeout, params=params)
        return res

    @staticmethod
    def post(
             url: str, headers: dict = {}, cookies: dict = None, timeout: int = 10, verify: bool = False,
            proxies: dict = None, data: dict = None, json: dict = None, params: dict = None
             ):

        if json is not None:
            res = requests.post(url, headers=headers, json=json, cookies=cookies, verify=verify, proxies=proxies,
                                timeout=timeout, params=params)
        elif data is not None:
            res = requests.post(url, headers=headers, data=data, cookies=cookies, verify=verify, proxies=proxies,
                                timeout=timeout, params=params)

        else:
            raise Exception("POST请求，未传入数据！！！！")

        return res

# class Session:
#     @staticmethod
#     def post()