import logging
import sys
sys.path.append("./")
import app_log_config

from fastapi import FastAPI, Request, UploadFile, File, Form

from model.alarm_model import AlarmModel
from model.defence_status import DefenceStatus

app = FastAPI()

CODE = 200
@app.get("/setcode/{code}")
async def set_code(code:int):
    global CODE
    CODE = code
    return {"code": CODE}


@app.post("/api/opticalfiber/alarm")
# https:// {ip}:{port}/perimeter/alarm
async def alarm(alarm_model: AlarmModel, request: Request):
    """
    报警函数
    :param alarm_model:
    :param request:
    :return:
    """
    logging.info(f"收到报警, 报警码:{alarm_model.alarmEventId}, 报警状态:{alarm_model.get_status()}, 报警位置:{alarm_model.position}")
    logging.info(alarm_model.model_dump())
    logging.info(dict(request).get("headers"))
    return {
        "code": CODE,
        "message": "OK",
        "data": ""
    }
@app.post("/api/opticalfiber/defenceStatus ")
async def defence_status(defence_status_model: DefenceStatus, request: Request):
    """
    报警函数
    :param defence_status_model:
    :param request:
    :return:
    """
    logging.info(f"收到防区状态, 是否报警:{defence_status_model.defenceStatus}, 图片地址:{defence_status_model.defenceImage}")
    logging.info(defence_status.model_dump())
    logging.info(dict(request).get("headers"))
    return {
        "code": CODE,
        "message": "OK",
        "data": ""
    }

@app.post("/api/upload")
async  def upload_file(request: Request, file: UploadFile = File(...),company: str = Form(...), date: str = Form(...)):
    """
    上传文件
    :param request:
    :param file:
    :param company:
    :param date:
    :return:
    """

    logging.info(dict(request).get("headers"))
    logging.info(f"厂家: {company}, 日期: {date} 文件名称: {file.filename}, 文件类型: {file.content_type}")
    # if CODE == 200:
    #     try:
    #         with open(f"./uploads/{file.filename}", "wb") as f:
    #             while chunk := await file.read(1024): f.write(chunk)
    #     finally:
    #         await file.close()
    return {
        "code": CODE,
        "message": "OK",
        "data": ""
    }

