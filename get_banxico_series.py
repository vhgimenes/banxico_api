"""
Módulo Responsável pelas funçõs de extração de séries da API do Banxico.
"""

import contextlib
import requests
import pandas as pd
import numpy as np
import xlwings as xw

def get_series_from_api(series, init=False, end=False):
    """
    Função criada para buscar séries históricas
    """
    token = '50f9ebb667490db19e4c82ecdd2ece53372d7fa2bdf74618a1624940fa0b1bff'
    serie_str = ','.join(series)
    url = f'https://www.banxico.org.mx/SieAPIRest/service/v1/series/{serie_str}' + '/datos/{y}/{z}'.format(y=init, z=end)

    print(url)
    headers = {'Bmx-Token': token}
    response = requests.get(url, headers=headers)
    status = response.status_code
    if status != 200:
        return print('Error en la consulta, codgio {erro}'.format(erro=status))
    raw_data = response.json()
    data = []
    for i in raw_data['bmx']['series']:
        serie = pd.DataFrame(i['datos'])
        serie['fecha'] = pd.to_datetime(serie['fecha'])
        with contextlib.suppress(Exception):
            serie['dato'] = serie['dato'].apply(lambda x: float(x))
        serie.columns = ["Data"] + [i['idSerie']]
        serie.set_index('Data', inplace=True)
        data.append(serie)
    df = pd.concat(data, axis=1)
    df = df[series]
    df = df.replace('N/E', np.nan)
    return df

