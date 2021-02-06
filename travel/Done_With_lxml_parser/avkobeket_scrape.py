# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
#
#
# def get_info(origin,destination):
#     res = requests.get("https://avtobeket.kg/routes/")
#     soup = BeautifulSoup(res.content,'lxml')
#     inter_national_bus_table = soup.find_all('table')[0]
#     Bus_routes_table = soup.find_all('table')[1]
#     talasavtov_kyrgzAvtobekti = soup.find_all('table')[2]
#     df1 = pd.read_html(str(inter_national_bus_table))[0]
#     df2 = pd.read_html(str(Bus_routes_table))[0]
#     df3 = pd.read_html(str(talasavtov_kyrgzAvtobekti))[0]
#     pd.set_option("display.max_rows", None, "display.max_columns", None)
#     df1.to_latex(index=False)
#     df2.to_latex(index=False)
#     df3.to_latex(index=False)
#     all_df = pd.concat([df1, df2, df3],axis=0)
#     all_dataframe = all_df.dropna(subset=[1])
#     cleaned_df = all_dataframe.drop(columns=[6,7,8])
#     print(cleaned_df)
#
#     return cleaned_df.loc[(cleaned_df[1] == origin+" – "+destination) | (cleaned_df[1] == origin+"-"+destination) | (cleaned_df[1] == origin+" — "+destination)]
#
#
#
#
# print(get_info('Бишкек','Ташкент'))

import pandas as pd
import requests
from bs4 import BeautifulSoup
import pickle

def get_info ( origin , destination ):
    res = requests.get( "https://avtobeket.kg/routes/" )
    soup = BeautifulSoup(res.content, 'lxml' )
    inter_national_bus_table = soup.find_all( 'table' )[ 0 ]
    Bus_routes_table = soup.find_all( 'table' )[ 1 ]
    talasavtov_kyrgzAvtobekti = soup.find_all( 'table' )[ 2 ]
    df1 = pd.read_html( str (inter_national_bus_table))[ 0 ]
    df2 = pd.read_html( str (Bus_routes_table))[ 0 ]
    df3 = pd.read_html( str (talasavtov_kyrgzAvtobekti))[ 0 ]
    pd.set_option( "display.max_rows" , None , "display.max_columns" , None )
    df1.to_latex( index = False )
    df2.to_latex( index = False )
    df3.to_latex( index = False )
    all_df = pd.concat([df1, df2, df3], axis = 0 )
    all_dataframe = all_df.dropna( subset =[ 1 ])
    cleaned_df = all_dataframe.drop( columns =[ 6 , 7 , 8 ])
    cleaned_df.to_pickle('pickles/avtobeket', compression='infer', protocol=5, storage_options=None)

    return cleaned_df.loc[(cleaned_df[ 1 ] == origin+ " – " +destination) | (cleaned_df[ 1 ] == origin+ "-" +destination) | (cleaned_df[ 1 ] == origin+ " — " +destination)]

print(get_info('Бишкек','Ташкент'))


