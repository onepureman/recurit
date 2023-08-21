# -*- coding:utf-8 -*-
# ☯ Author: Jingyq
# ☯ Email: woshijingyongqiang@163.com
# ☯ Date: 2023/2/22 9:26
# ☯ Notes:

from fastapi import APIRouter, responses, Form
router = APIRouter()
from tasks import run_task
from pydantic import BaseModel


# 定义传入的参数
class Item(BaseModel):
    proxies: str = None
    task_name: str
    model: bool = None


@router.post("/recruit")
def spider_tasks_api(
        item: Item  # 传入的json
        ):

    """
    批量定时任务接口
    """

    proxies = {"https": item.proxies} if item.proxies else None  # 处理proxies 的格式
    print("使用代理:", proxies)

    _run_status = spider_tasks_run(item.task_name, proxies, item.model)
    if _run_status is True:
        message = "数据抓取成功"
        success = True
        code = 200
    else:
        message = _run_status
        success = False
        code = 202

    return responses.JSONResponse(status_code=200,
                                  content={
                                      "code": code,
                                      "success": success,  # 数据抓取成功或者失败
                                      "message": message  # 数据抓取失败报错信息或成功提示信息
                                  })


def spider_tasks_run(
        task_name: str,  # 运行的程序名：shanxiService ———>> run_task.py ——>>  函数名称
        proxies: dict,
        model
        ):

    try:
        _run_status = getattr(run_task, task_name)(proxies=proxies, model=model)  # 调用函数并传参
    except AttributeError as e:
        _run_status = str(e)
    except Exception as e:
        _run_status = str(e)

    return _run_status
