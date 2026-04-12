#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :sql_engin.py
# @Time      :2026/3/9 22:07
# @Author    :zhouxiaochuan
# @Description:
from contextlib import asynccontextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# 格式：mysql+asyncmy://用户名:密码@主机:端口/数据库名?参数
DB_URL = "mysql+asyncmy://root:root@localhost:3306/of_alarm_info?charset=utf8mb4"

async_engine = create_async_engine(
    DB_URL ,
    pool_size=5,          # 连接池默认大小
    max_overflow=10)      # 连接池最大溢出数)


SessionLocal = sessionmaker[AsyncSession](
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)
@asynccontextmanager
async def get_db():
    db = SessionLocal()  # 创建 Session
    try:
        yield db  # 把 Session 交给 with 语句使用
    except Exception as e:
        await db.rollback()  # 出错时回滚事务
        raise e  # 抛出异常，方便排查
    finally:
        await db.close()  # 无论是否报错，最终关闭 Session
