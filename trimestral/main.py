from src.instances import config, logger

from src.constants import COLUMNS, TABLES_TO_UPDATE

from src.query_handler import create_update_query
from src.error_manager import send_email
from src.base_matriz_reader import fetch_base_matriz_excel
from src.quarter_calculator import (
    get_current_quarter_earliest_date,
    get_quarter_period
)

import sqlalchemy
import psycopg2
import pandas as pd 
import datetime as dt

CURRENT_YEAR = dt.datetime.now().year
CURRENT_MONTH = dt.datetime.now().month

FILE_NAME = config['excel_database']['file_name']
FOLDER_NAME = config['excel_database']['folder_name']
DB_URL = config['database_url']
NUMBER_OF_QUARTERS_AHEAD_PROJECTIONS = config['number_of_quarters_ahead_for_projections']

CURRENT_QUARTER = get_quarter_period(current_quarter_earliest_date=get_current_quarter_earliest_date())

def fetch_base_matriz_excel_to_update_sql_tables():
     
    base_quarterly_dataframe = fetch_base_matriz_excel(
        file_name=FILE_NAME,
        folder_name=FOLDER_NAME,
        columns=COLUMNS,
        sheet_name='BASE_TRIM'
    )

    engine = sqlalchemy.create_engine(DB_URL)

    with engine.connect() as connection:
    
        base_quarterly_dataframe = base_quarterly_dataframe[~base_quarterly_dataframe["Fecha"].isna()].reset_index(drop=True)
        non_nan_year_number_of_rows = len(base_quarterly_dataframe)

        for idx in range(non_nan_year_number_of_rows):

            period = base_quarterly_dataframe.loc[idx,'Fecha']

            if period == CURRENT_QUARTER:
                current_period_idx = idx
                break

        final_period_idx = current_period_idx + NUMBER_OF_QUARTERS_AHEAD_PROJECTIONS
        
        if final_period_idx >= non_nan_year_number_of_rows:
            final_period_idx = non_nan_year_number_of_rows - 1

        for idx in range(current_period_idx-70, final_period_idx+6):
            period = base_quarterly_dataframe.loc[idx,'Fecha']
            print(period)

            for table,columns_list in TABLES_TO_UPDATE.items():
                for column in columns_list:    
                    if column not in ["Venta total de vivienda social y no social (número)",	"Venta total de vivienda social (número)",	"Venta total de vivienda no social (número)"]:
                        continue
                    logger.info(f'Trying to update column {column}')
                    
                    value = pd.to_numeric(
                        base_quarterly_dataframe.loc[idx, column],
                        errors='coerce'
                    )

                    logger.info(f'\tValue for {column} is {value} of type {type(value)}')
                    
                    if pd.isna(value):
                        logger.info(f'\tSkipping [{column}] in table {table} for quarter {period}')
                        continue
                    
                    query = create_update_query(column, value, period, table)
                    connection.execute(sqlalchemy.text(query))
                    connection.commit()
                    logger.info(f'\tUpdated [{column}={value:.4f}] in table {table} for quarter {period}')

if __name__ == '__main__':
    try:
        fetch_base_matriz_excel_to_update_sql_tables()
        logger.info("Updated quarterly variables")
    except Exception as e:
        logger.exception(e)
        send_email(e)
