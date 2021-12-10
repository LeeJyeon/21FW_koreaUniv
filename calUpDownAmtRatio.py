#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 19:25:53 2021

@author: jihyunlee
"""

import os
import pandas as pd
import datetime
from datetime import timedelta, date

os.chdir('/Users/jihyunlee/KoreaUniv/21FW/IntroDS/00.프로젝트')

data_lotte = pd.read_csv('023530.csv',index_col=False)
data_cgv = pd.read_csv('079160.csv',index_col=False)
data_jcon = pd.read_csv('036420.csv',index_col=False)

movie = pd.read_csv('movie_list.csv')


def findDate(date , term , chg_base_yn ):
    date = str(date)
    target_date = datetime.datetime(int(date[:4]),int(date[5:7]),int(date[8:]))
    base_date = target_date
    if chg_base_yn == 'Y':
        base_date = base_date + timedelta(days=term)
    target_date = target_date + timedelta(days=term)
    return (base_date.strftime('%Y.%m.%d') , target_date.strftime('%Y.%m.%d'))


def calUpDownRatio(daynub , price_data):
    
    lst = []
    for index, row in movie.iterrows():
    

        cal_date = findDate(row[7], daynub , 'N')
        
        base_price = price_data [ price_data['날짜'] == cal_date[0] ]['종가']
        target_price = price_data [ price_data['날짜'] == cal_date[1] ]['종가']
       
        # base_price
        cnt = 1
        while (base_price.empty):
            #daynub 일자가 휴장이면, 익개장일 종가
            cal_date = findDate(row[7], daynub + cnt , 'Y')
            base_price = price_data [ price_data['날짜'] == cal_date[0] ]['종가']
            cnt += 1
            
            if cnt ==10:
                break
                
        # target_price
        cnt = 1
        while (target_price.empty):
            #daynub 일자가 휴장이면, 익개장일 종가
            cal_date = findDate(row[7], daynub + cnt , 'Y')
            target_price = price_data [ price_data['날짜'] == cal_date[1] ]['종가']
            cnt += 1
            
        tmp = (target_price.values - base_price.values) / base_price.values * 100 
        
        lst.append( tmp[0] )
    
    return lst


lotte_3_days = ( calUpDownRatio(3, data_lotte) )
lotte_7_days = ( calUpDownRatio(7, data_lotte) )
lotte_15_days = ( calUpDownRatio(15, data_lotte) )

cgv_3_days = ( calUpDownRatio(3, data_cgv) )
cgv_7_days = ( calUpDownRatio(7, data_cgv) )
cgv_15_days = ( calUpDownRatio(15, data_cgv) )

jcon_3_days = ( calUpDownRatio(3, data_jcon) )
jcon_7_days = ( calUpDownRatio(7, data_jcon) )
jcon_15_days = ( calUpDownRatio(15, data_jcon) )

movie['lotte_3_days'] = lotte_3_days
movie['lotte_7_days'] = lotte_7_days
movie['lotte_15_days'] = lotte_15_days

movie['cgv_3_days'] = cgv_3_days
movie['cgv_7_days'] = cgv_7_days
movie['cgv_15_days'] = cgv_15_days

movie['jcon_3_days'] = jcon_3_days
movie['jcon_7_days'] = jcon_7_days
movie['jcon_15_days'] = jcon_15_days

movie.to_csv("movice_list_add_ratio.csv")

