#!/usr/bin/env python
# -*- coding: utf-8 -*-

FONT_PATH = './fonts/msyh.ttf'
EXCEL_PATH = 'foo_data.xlsx'


CENSUS_NUM = 35589 	#第六次人口普查户数（2010）
POVERTY_NUM = 9515	#贫穷户数（2016）
AREA_POVERTY_LINE = str("{:.2f}".format(POVERTY_NUM/float(CENSUS_NUM)*100))+"%"

# print AREA_POVERTY_LINE
