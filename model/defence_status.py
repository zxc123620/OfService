#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :defence_status.py
# @Time      :2026/3/31 22:07
# @Author    :zhouxiaochuan
# @Description:
from pydantic import BaseModel


class DefenceStatus(BaseModel):
    deviceCode: str
    companyCode: str
    lineCode: int
    defenceStatus: int
    defenceImage: str
    reportTime: str
