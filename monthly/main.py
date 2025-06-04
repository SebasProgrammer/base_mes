from src.instances import config, logger

from src.constants import COLUMNS,MONTHS
from src.base_matriz_reader import fetch_base_matriz_excel

from src.query_handler import create_update_query
from src.error_manager import send_email

import sqlalchemy
import psycopg2

FILE_NAME = config['excel_database']['file_name']
FOLDER_NAME = config['excel_database']['folder_name']
DB_URL = config['database_url']

def fetch_base_matriz_excel_to_update_sql_tables():
    
    base_mes_dataframe = fetch_base_matriz_excel(
        file_name=FILE_NAME,
        folder_name=FOLDER_NAME,
        columns=COLUMNS,
        sheet_name='BASE_MES'
    )

    engine = sqlalchemy.create_engine(DB_URL)
    with engine.connect() as connection:
        
        num_rows = len(base_mes_dataframe)
        for idx in range(num_rows-8, num_rows):
            for column in base_mes_dataframe.columns:
            
                if column not in ['Tipo de cambio de Bolivia (boliviano por US$, pdp)']:
                    continue

                year = base_mes_dataframe.loc[idx,'Año']

                print(year)
                
                month_name = base_mes_dataframe.loc[idx, 'Mes']
                month_number = 1+MONTHS.index(month_name)
                value = base_mes_dataframe.loc[idx, column]

                query = create_update_query(column, value, int(year), month_number)
                
                if query:
                    connection.execute(sqlalchemy.text(query))
                    # connection.commit()
                
                try:
                    logger.info(f'Updated {column} = {value:.4f} for period {month_name}/{int(year)}')
                except:
                    logger.info(f'Updated {column} = NULL for period {month_name}/{int(year)}')

if __name__ == '__main__':
    try:
        fetch_base_matriz_excel_to_update_sql_tables()
        logger.info("Updated monthly variables")
    except Exception as e:
        logger.exception(e)
        send_email(e)
