import datetime
import logging
import re
import sys
from math import lgamma

from sqlalchemy import Select

from sql_engin import get_db
from sql_model import OFAlarm

sys.path.append("./")
import app_log_config

from fastapi import FastAPI, Request, UploadFile, File, Form

from model.alarm_model import AlarmModel
from model.defence_status import DefenceStatus

app = FastAPI()


CODE = 200


@app.get("/setcode/{code}")
async def set_code(code: int):
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
    logging.info(
        f"收到报警, 报警码:{alarm_model.alarmEventId}, 报警状态:{alarm_model.get_status()}, 报警位置:{alarm_model.position}")
    alarm_event_id = re.sub("_(.*?)_",lambda m: "_DevNo_",alarm_model.alarmEventId)
    alarm_id = re.sub("_(.*?)_",lambda m:"_DevNo_",alarm_model.alarmId)
    select = Select(OFAlarm).where(
        OFAlarm.event_id == alarm_event_id,
        OFAlarm.alarm_id == alarm_id,
        OFAlarm.alarm_status == alarm_model.alarmStatus)
    async with get_db() as session:
        of_alarm = await session.scalar(select)
        if of_alarm:
            of_alarm.server_recv = 1
            alarm_image =re.findall(r"/(event.*\.(?:jpg|png))$",alarm_model.alarmImage)
            of_alarm.alarm_image = alarm_image[0] if alarm_image else None
            logging.info("将报警消息置为已收到并存储报警图片地址")
            await session.commit()
        else:
            logging.info("没在数据库中找到报警")

    logging.info(alarm_model.model_dump())
    logging.info(dict(request).get("headers"))
    return {
        "code": CODE,
        "message": "OK",
        "data": ""
    }


@app.post("/api/defencestatus")
async def defence_status(defence_status_model: DefenceStatus, request: Request):
    """
    报警函数
    :param defence_status_model:
    :param request:
    :return:
    """
    logging.info(
        f"收到防区状态, 是否报警:{defence_status_model.defenceStatus}, 图片地址:{defence_status_model.defenceImage}")
    logging.info(defence_status_model.model_dump())
    logging.info(dict(request).get("headers"))
    return {
        "code": CODE,
        "message": "OK",
        "data": ""
    }


@app.post("/api/upload")
async def upload_file(request: Request, file: UploadFile = File(...), company: str = Form(...), date: str = Form(...)):
    """
    上传文件
    :param request:
    :param file:
    :param company:
    :param date:
    :return:
    """

    logging.info(dict(request).get("headers"))
    logging.info(
        f"收到报警图片 ,厂家: {company}, 日期: {date} 文件名称: {file.filename}, 文件类型: {file.content_type}")
    # device_id, event_id, time_id, alarm_status = re.findall("event_(.*?)_(.*?)_(.*?)_(.+).jpg", "file.filename") # event_51939169135051020004_e11011221_20260411150443_1
    select = Select(OFAlarm).where(OFAlarm.alarm_image == file.filename)
    async with get_db() as session:
        alarm_sql_model = await session.scalar(select)
        if alarm_sql_model:
            logging.info("将报警图片设置为已收到")
            alarm_sql_model.image_recv = 1
            alarm_sql_model.image_recv_time = datetime.datetime.now()
            await session.commit()
        else:
            logging.info("没有找到报警图片对应的报警")
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="10.168.2.209", port=8000)
