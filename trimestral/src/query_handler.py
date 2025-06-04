import pandas as pd
from .constants import TABLES_TO_UPDATE
from .rename import normalize_name, remove_tildes
from .instances import logger

def create_update_query(column_name:str, value:float, period:str, table_name:str) -> str:
 
    new_column_name = normalize_name( remove_tildes(column_name) )    

    set_query = f'{new_column_name} = {value:.4f}'
    
    condition = """WHERE fecha = '{}'""".format(period) 
    query = f'UPDATE {table_name} SET {set_query} {condition};'

    return query