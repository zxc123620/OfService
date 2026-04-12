#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :sql_model.py
# @Time      :2026/3/9 21:39
# @Author    :zhouxiaochuan
# @Description:
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column

Base = declarative_base()

class OFAlarm(Base):
    __tablename__ = "of_alarm"  # 对应数据库表名
    # alarm_data_id = Column(String(36), primary_key=True)
    alarm_data_id : Mapped[str]= mapped_column(String(100), primary_key=True)
    event_id : Mapped[str] = mapped_column(String(100))
    alarm_id : Mapped[str] = mapped_column(String(100))
    alarm_status: Mapped[int] = mapped_column(Integer)
    alarm_time : Mapped[datetime] = mapped_column(DateTime)
    recv : Mapped[int] = mapped_column(Integer, default=0)
    server_recv : Mapped[int] = mapped_column(Integer, default=0)
    alarm_image: Mapped[str] = mapped_column(String(255))
    image_recv : Mapped[int] = mapped_column(Integer, default=0)
    position : Mapped[int] = mapped_column(Integer, default=0)
    image_recv_time : Mapped[datetime] = mapped_column(DateTime)