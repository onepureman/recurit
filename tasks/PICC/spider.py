# -*- coding:utf-8 -*-
# ☯ Author: Jingyq
# ☯ Email: woshijingyongqiang@163.com
# ☯ Date: 2023/8/21 12:53
# ☯ Notes:
from common.base_spider import BaseSpider
from util.requests_util import Requests as requests
from typing import Dict, NoReturn, Any, List
from common import config
from lxml import etree
from util.sql import CreateConnect


class PICCSpider(BaseSpider):
    """"""

    def __init__(self, model) -> NoReturn:
        self.spider_params = config.spider_params
        self.base_url = "https://picc.zhiye.com/"
        self.model = model
        self.Create_Connect = CreateConnect(collection_name="spider_data")

    def _downloader(self, request_params: Dict[str, Any],) -> Dict[str, Any]:

        res = requests.get(request_params["url"], verify=False, proxies=request_params["proxies"], timeout=60)

        return res.content.decode()

    def _parser(self, request_params: Dict[str, Any], response: Dict[str, Any]) -> List[Any]:
        flag = False
        html = etree.HTML(response)

        job_list = html.xpath("//div[@class='job-list']/div")
        for one_div in job_list:
            one_left_div = one_div.xpath("./div[@class='top']/div[@class='left']")[0]

            data_index = {
            "top": one_left_div.xpath("./div[@class='t']/text()")[0],
            "department": one_left_div.xpath("./div[@class='b']/span[1]/text()")[0],
            "address": one_left_div.xpath("./div[@class='b']/span[3]/text()")[0].replace(",", "|"),
            "publish_date": one_left_div.xpath("./div[@class='b']/span[5]/text()")[0],
            "from": "PICC"
            }

            data = {
                    "zhize": "\n".join(one_div.xpath("./div[@class='con']/div/h5[contains(text(), '岗位职责：')]/../p/text()")),
                    "yaoqiu": "\n".join(one_div.xpath("./div[@class='con']/div/h5[contains(text(), '任职要求：')]/../p/text()")),
                }
            data.update(data_index)


            res = self.Create_Connect.mongo_db_find_one(data_index)

            if res is None:
                self.Create_Connect.mongo_db_insert_one(data)
            else:

                if self.model == "increment":
                    return flag, data
                else:
                    self.Create_Connect.mongo_db_update_one(data_index, data)



        url_n = html.xpath("//div[@class='pager']//a[text()='下一页']/@href")
        if len(url_n) > 0:
            flag = True
            request_params["url"] = self.base_url + url_n[0]


        return flag, "data"

    def _pipeline(self, request_params: Dict[str, Any], data: List[Any]) -> bool:


        return True

    def run(self, request_params):

        super().spider_next(request_params)





