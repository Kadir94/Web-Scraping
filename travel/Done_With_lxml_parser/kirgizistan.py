import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
from google_trans_new import google_translator
from configurations.settings import DARK_PURPLE, ENDE, INBOX, LIGHT_BLUE
from typing import Dict
from logging import Logger
import pickle


def get_info(page,
             country_id: int,
             origin: str,
             origin_id: int,
             destination: str,
             destination_id: int,
             total_size: int,
             hash_id: str,
             order: int,
             date: str,
             logger: Logger) -> Dict:

    translator = google_translator()
    translated_origin = translator.translate(origin, lang_src='en', lang_tgt='ru')
    translated_dest = translator.translate(destination, lang_src='en', lang_tgt='ru')
    date = None
    list_dict = []
    res = requests.get("https://avtobeket.kg/routes/")
    soup = BeautifulSoup(res.content,'lxml')
    Bus_routes_table = soup.find_all('table')[1]
    df2 = pd.read_html(str(Bus_routes_table))[0]
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    df2.to_latex(index=False)
    all_df = pd.concat([df2],axis=0)
    all_dataframe = all_df.dropna(subset=[1])
    all_dataframe.to_pickle('avtobeket.pickle', compression='infer', protocol=5, storage_options=None)
    df_from_pickle = pd.read_pickle("avtobeket.pickle")
    print(df_from_pickle)
    data = all_dataframe.loc[(all_dataframe[1] == translated_origin+" – "+translated_dest) | (all_dataframe[1] == translated_origin+"-"+translated_dest) | (all_dataframe[1] == translated_origin+" — "+translated_dest)]
    print(data)
    list_dict.append({
            'date': date,
            'departureTime': data[2].values,
            'arrivalTime': None,
            'price': data[4].values
    })
    total_data = {
        'country_id': country_id,
        'origin_id': origin_id,
        'destination_id': destination_id,

        'data': list_dict,
        'total_size': total_size,
        'order': order,
        'hash_id': hash_id,
        'status': 200  # Success
    }
    return total_data


get_info(page=None,
         country_id=1233,
         origin='Талас',
         origin_id=345,
         destination='Маймак',
         destination_id=234,
         total_size=5,
         hash_id='dsfg32',
         order=2,
         date='13-05-2021',
         logger=None)
