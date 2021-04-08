import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
from googletrans import Translator
from typing import Dict
from logging import Logger
import pickle
import os


def get_info(origin: str, destination: str,
             page=None,
             origin_id: int = None, destination_id: int = None,
             total_size: int = None, hash_id: str = None,
             order: int = None, date: str = None, logger: Logger = None) -> Dict:
    list_dict = []
    translator = Translator()
    translated_origin = translator.translate(origin, src='en', dest='ru').text
    translated_dest = translator.translate(destination, src='en', dest='ru').text
    if not os.path.isdir('./pickles/avtobeket.pickle'):
        res = requests.get("https://avtobeket.kg/routes/")
        soup = BeautifulSoup(res.content, 'lxml')
        bus_routes_table = soup.find_all('table')[1]
        df2 = pd.read_html(str(bus_routes_table))[0]
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        df2.to_latex(index=False)
        df2 = df2.dropna(subset=[1])
        df2.to_pickle('avtobeket.pickle', compression='infer', protocol=5)
        data = df2.loc[
            (df2[1] ==
             translated_origin + " – " + translated_dest) |
            (df2[1] == translated_origin + "-" + translated_dest) |
            (df2[1] == translated_origin + " — " + translated_dest)
            ]
    else:
        df = pd.read_pickle('pickles/avtobeket.pickle')
        data = df.loc[
            (df[1] ==
             translated_origin + " – " + translated_dest) |
            (df[1] == translated_origin + "-" + translated_dest) |
            (df[1] == translated_origin + " — " + translated_dest)
            ]

    prices = data[4].values
    dep_info = data[2].values
    if len(prices) > 0:
        for departure,prce in zip(dep_info,prices):
            price = float(prce)
            price = price / 100
            list_dict.append({
                'date': date,
                'departure_time': departure,
                'arrival_time': None,
                'price': price
            })
        total_data = {
            'origin_id': origin_id,
            'destination_id': destination_id,
            'data': list_dict,
            'total_size': total_size,
            'order': order,
            'hash_id': hash_id,
            'status': 200  # Success
        }
        print(total_data)
    else:
        return Response(
            origin_id=origin_id,
            destination_id=destination_id,
            data=list_dict,
            total_size=total_size,
            date=date,
            order=order,
            hash_id=hash_id,
            status=400  # Not found
        )


# get_info(page=None,origin='Talas',origin_id=None, destination='Bishkek Taraz',destination_id=None,total_size=None,hash_id=None,order=None,date=None,logger=Logger)
