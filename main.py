# -*- encoding: utf-8 -*-
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
import streamlit as st
import loggerConfig
import pandas as pd
from crawlDou import crawlDou
from writeResult import writeResult
import os.path
import base64
from datetime import date

data_atual = date.today()

data = '{}-{}-{}'.format(data_atual.day, data_atual.month, data_atual.year)

# create a crawler process with the specified settings
runner  = CrawlerRunner(
    {
        'LOG_STDOUT': False,
        'LOG_ENABLED': True,
        'ROBOTSTXT_OBEY' : True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 5,
        'RETRY_TIMES' : 5,
        'AUTOTHROTTLE_ENABLED' : True,
        'HTTPCACHE_ENABLED': True,  # for development
        'FEEDS':{
            'items.jl': {
                'format': 'jsonlines',
                'encoding': 'utf8'
            }   
        },
    }
)

dou = st.text_input('Para ATOS NORMATIVOS escreva dou1, para ATOS DE PESSOAL escreva dou2, para CONTRATOS, EDITAIS E AVISOS escreva dou1', 'dou1')
st.write('Aguarde o processo para baixar o csv', dou)

crawlDou(runner, data, 'dou1')
reactor.run()

if (os.path.exists("items.jl")):
    writeResult("result.json", "items.jl")
else:
    raise FileNotFoundError("Required files not found. Try again later")


def get_table_download_link_csv(df):
    csv = pd.read_json(df)
    csv = csv.to_csv().encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="captura.csv" target="_blank">Download csv file</a>'
    return href
df = "result.json"
st.markdown(get_table_download_link_csv(df), unsafe_allow_html=True)
