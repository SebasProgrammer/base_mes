import pandas as pd
from .constants import TABLE_NAMES_PER_COLUMN
from .rename import rename_mensual

def create_update_query(column_name:str, value:float, year:int, month:int) -> str:

    table_name = TABLE_NAMES_PER_COLUMN[column_name]
    new_column_name = rename_mensual(column_name)
    
    if pd.isna(value) or isinstance(value,str):
        value = 'NULL'
        set_query = f'"{new_column_name}" = {value}'
        return ''
    else:
        set_query = f'"{new_column_name}" = {value:.4f}'
    
    condition = """WHERE "Fecha" = '{}-{:02}-01'""".format(year, month) 
    query = f'UPDATE {table_name} SET {set_query} {condition};'
    return query