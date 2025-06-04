from src.sharepoint_api import SharePoint
from io import BytesIO

import pandas as pd


def fetch_base_matriz_excel(folder_name:str, file_name:str, columns:list[str], sheet_name:str) -> pd.DataFrame:

    file_obj = SharePoint().download_file(file_name, folder_name)
    base_mes_dataframe = pd.read_excel(
        BytesIO(file_obj), 
        sheet_name = sheet_name, 
        usecols = columns, 
        header = 0,
        engine='openpyxl'
    )

    return base_mes_dataframe