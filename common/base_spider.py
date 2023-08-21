import datetime
from typing import Dict, List, Any, NoReturn
from abc import ABCMeta, abstractmethod
import time
import logging
logging.basicConfig(level=logging.INFO)
from common.logger.logger import logger
from common import config

class BaseSpider(metaclass=ABCMeta):
    """爬虫公共基类"""

    def __init__(self, spider_params) -> NoReturn:
        """
            构造方法
            参数:
                spider_params: 爬虫配置相关参数 包括max_retry_times和download_delay_time
            返回值：
                None
        """
        self.spider_params = spider_params


    @abstractmethod
    def _downloader(self, request_params: Dict[str, Any]) -> Dict[str, Any]:
        """
            数据爬取方法
            参数:
                request_params: 爬虫爬取相关参数
            返回值:
                下载器下载到的数据 字典类型 键为 html json 或者bytes_stream 如果爬取失败返回None
        """

    @abstractmethod
    def _parser(self, request_params: Dict[str, Any], response: Dict[str, Any]) -> List[Any]:
        """
            数据解析方法
            参数:
                response: 下载器返回的内容，字典类型
            返回值:
                解析出的数据列表 List类型 如果解析失败返回None
        """

    @abstractmethod
    def _pipeline(self, request_params: Dict[str, Any], data: List[Any]) -> bool:
        """
            数据管道方法
            参数:
                data: 解析出的数据 List类型
            返回值:
                数据入库状态 已入库返回True 入库失败返回False
        """

    def spider(self, request_params: Dict[str, Any] = None) -> NoReturn:
        """
            爬虫引擎
            参数：
                request_params: 爬虫请求参数，字典类型
            返回值：
                无
        """
        log_template = '[spider] {0}  [time] {1}  [params] {2}  [info] {3}'  # 日志模板
        class_name = self.__class__.__name__  # 获取爬虫类名

        # 获取配置信息或设置默认参数
        max_retry_times = self.spider_params.get('max_retry_times') or 3  # 最大下载重试次数 默认3次
        download_delay_time = self.spider_params.get('download_delay_time') or 3  # 下载器休眠时间
        # 下载过程

        response = None
        for i in range(max_retry_times):
            logger.info(log_template.format(class_name, datetime.datetime.now(), request_params, '第{}次请求'.format(i + 1)))
            response = self._downloader(request_params)
            time.sleep(download_delay_time)
            if response:
                break

        if not response:  # 多次尝试下载均失败的情况
            logger.error(log_template.format(class_name, datetime.datetime.now(), request_params, '下载失败'))
            return
        else:
            logger.info(log_template.format(class_name, datetime.datetime.now(), request_params, '下载成功'))

        # 解析过程
        data = self._parser(request_params, response)
        if not data:
            logger.error(log_template.format(class_name, datetime.datetime.now(), request_params, '解析失败'))
            return

        elif len(data) == 1 and isinstance(data[0], dict) and data[0].get('error_info'):
            logger.error(log_template.format(class_name, datetime.datetime.now(), request_params, '解析失败: ' + data[0].get('error_info')))
            return
        else:
            logger.info(log_template.format(class_name, datetime.datetime.now(), request_params, '解析成功'))

        # 入库过程
        is_success = self._pipeline(request_params, data)
        info = '已爬取{0}条数据'.format(len(data)) if is_success else '入库失败'
        logger.info(log_template.format(class_name, datetime.datetime.now(), request_params, info))

    def spider_next(self, request_params: Dict[str, Any] = None) -> NoReturn:
        """
            爬虫引擎, 包含翻页 逻辑
            参数：
                request_params: 爬虫请求参数，字典类型
            返回值：
                无
        """
        log_template = '[spider] {0}  [time] {1}  [params] {2}  [info] {3}'  # 日志模板
        class_name = self.__class__.__name__  # 获取爬虫类名

        # 获取配置信息或设置默认参数
        max_retry_times = self.spider_params.get('max_retry_times') or 3  # 最大下载重试次数 默认3次
        download_delay_time = self.spider_params.get('download_delay_time') or 3  # 下载器休眠时间
        # 下载过程


        while 1:

            response = None
            for i in range(max_retry_times):
                logger.info(log_template.format(class_name, datetime.datetime.now(), request_params, '第{}次请求'.format(i + 1)))
                response = self._downloader(request_params)
                time.sleep(download_delay_time)
                if response:
                    break

            if not response:  # 多次尝试下载均失败的情况
                logger.error(log_template.format(class_name, datetime.datetime.now(), request_params, '下载失败'))
                return
            else:
                logger.info(log_template.format(class_name, datetime.datetime.now(), request_params, '下载成功'))

            # 解析过程
            flag, data = self._parser(request_params, response)
            if not data:
                logger.error(log_template.format(class_name, datetime.datetime.now(), request_params, '解析失败'))
                return

            elif len(data) == 1 and isinstance(data[0], dict) and data[0].get('error_info'):
                logger.error(log_template.format(class_name, datetime.datetime.now(), request_params, '解析失败: ' + data[0].get('error_info')))
                return
            else:
                logger.info(log_template.format(class_name, datetime.datetime.now(), request_params, '解析成功'))

            if not flag:  # 标识是否继续请求
                break


        # 入库过程
        # is_success = self._pipeline(request_params, data)
        # info = '已爬取{0}条数据'.format(len(data)) if is_success else '入库失败'
        # logger.info(log_template.format(class_name, datetime.datetime.now(), request_params, info))


