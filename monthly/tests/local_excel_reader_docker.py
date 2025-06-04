from src.instances import config, logger

from src.sharepoint_api import SharePoint

import pandas as pd

FILE_NAME = config['excel_database']['file_name']
FOLDER_NAME = config['excel_database']['folder_name']

def main():
    
    sheet = 'BASE_MES'
    download_path = 'Base Matriz.xlsm'
    SharePoint().download_file_locally(FILE_NAME, FOLDER_NAME, download_path)
    base_mes_dataframe = pd.read_excel(
        download_path,
        sheet_name=sheet,
        engine='openpyxl'
    )
    logger.info(base_mes_dataframe.shape)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.exception(e)
