from src.instances import config, logger

from src.constants import COLUMNS, TABLES_TO_UPDATE

from src.query_handler import create_update_query
from src.error_manager import send_email
from src.base_matriz_reader import fetch_base_matriz_excel

import sqlalchemy
import psycopg2
import pandas as pd 
import datetime as dt

CURRENT_YEAR = dt.datetime.now().year
FILE_NAME = config['excel_database']['file_name']
FOLDER_NAME = config['excel_database']['folder_name']
DB_URL = config['database_url']
NUMBER_OF_YEARS_AHEAD_PROJECTIONS = config['number_of_years_ahead_for_projections']

def fetch_base_matriz_excel_to_update_sql_tables():
     
    base_anual_dataframe = fetch_base_matriz_excel(
        file_name=FILE_NAME,
        folder_name=FOLDER_NAME,
        columns=COLUMNS,
        sheet_name='BASE_ANUAL'
    )

    engine = sqlalchemy.create_engine(DB_URL)

    with engine.connect() as connection:
    
        base_anual_dataframe = base_anual_dataframe[~base_anual_dataframe["Año"].isna()].reset_index(drop=True)
        non_nan_year_number_of_rows = len(base_anual_dataframe)

        for idx in range(non_nan_year_number_of_rows):

            year = int(base_anual_dataframe.loc[idx,'Año'])

            if year == CURRENT_YEAR:
                current_year_idx = idx
                break

        final_year_idx = current_year_idx + NUMBER_OF_YEARS_AHEAD_PROJECTIONS
        
        if final_year_idx >= non_nan_year_number_of_rows:
            final_year_idx = non_nan_year_number_of_rows - 1

        for idx in range(current_year_idx-6, final_year_idx+1):
            year = base_anual_dataframe.loc[idx,'Año']
            print(year)
            for table,columns_list in TABLES_TO_UPDATE.items():
                for column in columns_list:
                    if column not in ["PBI nominal (US$ millones)","PBI (Var.% real)","Demanda interna (Var.% real)","Crédito de consumo (Var.% nominal anual)","Consumo privado (Var.% real)","Consumo público (Var.% real)","Inversión privada (Var.% real)","Inversión pública (Var.% real)","Inversión total (Var.% real)","Exportaciones (Var.% real)","Importaciones (Var.% real)","PBI primario (Var.% real)","PBI no primario (Var.% real)","PBI Agropecuario (Var.% real)","PBI Agrícola (Var.% real)","PBI Pecuario (Var.% real)","PBI Pesca (Var.% real)","PBI Manufactura (Var.% real)","PBI Manufactura no primaria (Var.% real)","PBI Manufactura primaria (Var.% real)","Minería e Hidrocarburos (Var.% real)","PBI Hidrocarburos (Var.% real)","PBI Minería  (Var.% real)","PBI Comercio (Var.% real)","PBI Construcción (Var.% real)","PBI Servicios (Var.% real)","Inflación (%, fdp)","Inflación, promedio de período (%)","Resultado fiscal (% del PBI)","Deuda pública (% del PBI)","Cuenta corriente (% del PBI)","Tipo de cambio, fin de período (S/ por US$)","Tipo de cambio, promedio de período (S/ por US$)","Índice de precios al consumidor Lima Metropolitana","Importación de bienes de capital, sin materiales de construcción (Var.% real)","Consumo interno de cemento (Var.%)","Consumo total (Var.% real)","PBI per cápita (US$)","Gasto público en construcción total (Var. % real)","Gasto público en construcción Lima (Var. % real)","Gasto público en construcción Zona Norte (Var. % real)","Gasto público en construcción Zona Sur (Var. % real)","Gasto público en construcción Zona Oriente (Var. % real)","Gasto público en construcción Zona Centro (Var. % real)","PBI Nacional (S/ Miles del 2007)","PBI Nacional no primario (S/Miles del 2007)","PBI Nacional no primario (Var. % real)","PBI Nacional agropecuario (S/ Miles del 2007)","PBI Nacional Pesca (S/ Miles del 2007)","PBI Nacional Minería e hidrocarburos (S/ Miles del 2007)","PBI Nacional Manufactura (S/ Miles del 2007)","PBI Nacional Electricidad (S/ Miles del 2007)","PBI Nacional Construcción (S/ Miles del 2007)","PBI Nacional Comercio (S/ Miles del 2007)","PBI Nacional Transporte (S/ Miles del 2007)","PBI Nacional Alojamiento y restaurante (S/ Miles del 2007)","PBI Nacional Telecomunicaciones (S/ Miles del 2007)","PBI Nacional Administración pública (S/ Miles del 2007)","PBI Nacional Otros servicios (S/ Miles del 2007)","PBI Nacional agropecuario (Var. % real)","PBI Nacional Pesca (Var. % real)","PBI Nacional Minería e hidrocarburos (Var. % real)","PBI Nacional Manufactura (Var. % real)","PBI Nacional Electricidad (Var. % real)","PBI Nacional Construcción (Var. % real)","PBI Nacional Comercio (Var. % real)","PBI Nacional Transporte (Var. % real)","PBI Nacional Alojamiento y restaurante (Var. % real)","PBI Nacional Telecomunicaciones (Var. % real)","PBI Nacional Administración pública (Var. % real)","PBI Nacional Otros servicios (Var. % real)","PBI nominal (Var. %)","PBI real (Millones de S/ del 2007)","PBI nominal (Millones de S/)","Demanda interna sin inventarios (Var.% real)"]:
                        continue
                    
                    value = base_anual_dataframe.loc[idx, column]
                    print(value)
                    if pd.isna(value) or isinstance(value,str):
                        logger.info(f'Skipping [{column}] in table {table} for period {year}')
                        continue
                    
                    query = create_update_query(column, value, int(year), table)
                    # print(query)
                    # print(table, column)
                    if query:
                        connection.execute(sqlalchemy.text(query))
                        connection.commit()
                
                    logger.info(f'Updated [{column}={value:.4f}] in table {table} for period {year}')

if __name__ == '__main__':
    try:
        fetch_base_matriz_excel_to_update_sql_tables()
        logger.info("Updated annually variables")
    except Exception as e:
        logger.exception(e)
        send_email(e)
