#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 11:55:50 2021

@author: jihyunlee
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests



def price(code):
    last_page = 100
    
    df = pd.DataFrame()
    sise_url = 'https://finance.naver.com/item/sise_day.nhn?code='+code
    
    for page in range(1, int(last_page)+1):
        page_url = '{}&page={}'.format(sise_url, page)
        response_page = requests.get(page_url, headers={'User-agent': 'Mozilla/5.0'}).text
        df = df.append(pd.read_html(response_page)[0])
    
    df = df.dropna() # n/a 제거
    df = df.reset_index(drop=True) # 인덱스 리셋
    df.to_csv(code + '.csv')
    print('good '+code)


price( '023530' ) #롯데쇼핑
price( '079160' ) #cgv
price( '036420' ) #제이콘텐트리



