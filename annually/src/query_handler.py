import pandas as pd
from .constants import TABLES_TO_UPDATE
from .rename import normalize_name, remove_tildes

def create_update_query(column_name:str, value:float, year:int, table_name:str) -> str:
 
    new_column_name = normalize_name( remove_tildes(column_name) )
    
    if pd.isna(value):
        value = 'NULL'
        set_query = f'{new_column_name} = {value}'
        return ''
    else:
        set_query = f'{new_column_name} = {value:.4f}'
        
    condition = """WHERE fecha = {}""".format(year) 
    query = f'UPDATE {table_name} SET {set_query} {condition};'

    return query