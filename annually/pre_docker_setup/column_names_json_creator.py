from src.instances import config, logger
from src.sharepoint_api import SharePoint
from src.rename import normalize_name, remove_tildes
from src.base_matriz_reader import fetch_base_matriz_excel

import pandas as pd
import sqlalchemy
import psycopg2
import re
import json

from unicodedata import normalize
from io import BytesIO
from collections import defaultdict

FILE_NAME = config['excel_database']['file_name']
FOLDER_NAME = config['excel_database']['folder_name']
DB_URL = config['database_url']

FIND_TABLE_WITH_CONTAINS_COLUMN_NAME = """SELECT t.table_name
FROM information_schema.tables t
INNER JOIN information_schema.columns c ON c.table_name = t.table_name 
                                AND c.table_schema = t.table_schema
WHERE c.column_name = '{column_name}'
      AND t.table_schema NOT IN ('information_schema', 'pg_catalog')
      AND t.table_type = 'BASE TABLE'
ORDER BY t.table_schema;"""

def get_json_file_of_variables(annually_variables:list) -> dict:
    
    file_obj = SharePoint().download_file(FILE_NAME, FOLDER_NAME)
    sheet = 'BASE_ANUAL'
    base_anual_dataframe = pd.read_excel(
        BytesIO(file_obj), 
        sheet_name = sheet, 
        header = 0, 
        usecols = lambda variable : variable in annually_variables)

    engine = sqlalchemy.create_engine(DB_URL)

    tables_dictionary = defaultdict(list)

    with engine.connect() as connection:
        for column in base_anual_dataframe.columns:

            if column in ['Frecuencia','Año','Periodo','Fecha']:
                continue

            column_sin_tilde = remove_tildes(column)
            column_sql = normalize_name(column_sin_tilde)
            #print(f'{column} : {column_sql}')
            query = FIND_TABLE_WITH_CONTAINS_COLUMN_NAME.format(column_name = column_sql)

            try:
                table_names = connection.execute(sqlalchemy.text(query)).fetchall()

                if table_names == []:
                    logger.warning(f'{column} with {column_sql} is not in any table')
                    continue

                for table in table_names:
                    if re.search(r'anual\b', table[0]):
                        logger.info(f'There is anual table for var {column_sql}')
                        table_name = table[0]
                    else:
                        table_name = None
            except:
                table_name = None

            if table_name:
                tables_dictionary[table_name].append(column)
                logger.info(f'{column} with {column_sql} is in table [{table_name}]')
            else: 
                logger.warning(f'{column} with {column_sql} is not in any table')
    
    return tables_dictionary
    
def get_only_anual_columns():
    
    variables_file_name = 'Variables BM y encargados.xlsx'
    variables_folder_name = "05. Encargos regulares"
    variables_file_obj = SharePoint().download_file(variables_file_name, variables_folder_name)
    sheet = 'Variables de BM'
    vars_to_use = []
    variables_dataframe = pd.read_excel(
        BytesIO(variables_file_obj), 
        sheet_name = sheet, header = 0, 
        usecols = [
            'Variable', 
            'Mensual', 
            'Trimestral', 
            'Anual', 
            '¿Listo en SQL? 1=sí; 0=no'])
    vars_to_use_dataframe = variables_dataframe.loc[ 
        (variables_dataframe['Anual'] == 1) 
        #(variables_dataframe['Mensual'] != 1) &
        #(variables_dataframe['Trimestral'] != 1) &
        #(variables_dataframe['¿Listo en SQL? 1=sí; 0=no'] != 1) 
    ]

    return vars_to_use_dataframe['Variable'].tolist()

if __name__ == '__main__':
    
    annually_variables = get_only_anual_columns()

    with open('src/columns.json', 'w', encoding='utf-8') as file: 
        json.dump(annually_variables, file, ensure_ascii=False, indent=2)

    variables_dictionary_json = get_json_file_of_variables(annually_variables)

    file_to_dump_json = 'src/tables_to_update.json'
    with open(file_to_dump_json, 'w', encoding='utf-8') as json_file: 
        json.dump(variables_dictionary_json, json_file, ensure_ascii=False, indent=2)
