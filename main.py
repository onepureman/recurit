# -*- coding:utf-8 -*-
# ☯ Author: Jingyq
# ☯ Email: woshijingyongqiang@163.com
# ☯ Date: 2023/8/21 12:25
# ☯ Notes:


from fastapi import FastAPI, responses
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from service import spider_tasks

app = FastAPI(title="爬虫接口", version="0.0.1", docs_url="/api/fastapi/docs")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return responses.JSONResponse(
        status_code=200,
        content={
            "code": 202,
            "success": False,  # 数据抓取成功或者失败
            "message": "参数错误或丢失"  # 数据抓取失败报错信息或成功提示信息
        }

    )

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(spider_tasks.router)  # 登录接口


if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=False, host="0.0.0.0", port=8001)


