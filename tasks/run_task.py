# -*- coding:utf-8 -*-
# ☯ Author: Jingyq
# ☯ Email: woshijingyongqiang@163.com
# ☯ Date: 2023/2/22 11:08
# ☯ Notes:
from tasks.PICC.spider import PICCSpider


def PICC_spider_task(proxies, model):

    spider = PICCSpider(model)
    spider.run({
        "proxies": proxies,
        "url": "https://picc.zhiye.com/xzlist3/?d=-1&p=1%5E-1%2C3%5E-1&PageIndex=1",  # 首页地址
    })
    spider.run({
        "proxies": proxies,
        "url": "https://picc.zhiye.com/shixi/?PageIndex=1",  # 首页地址
    })
    spider.Create_Connect.close_connect()

    return True


if __name__ == '__main__':

    PICC_spider_task("", model='increment')
