# -*- coding: utf-8 -*-
from datetime import datetime


def convert_string_to_datetime(time_string):
    year = int(time_string[:4])
    month = int(time_string[5:7])
    day = int(time_string[8:10])
    return datetime(year=year, month=month, day=day)
