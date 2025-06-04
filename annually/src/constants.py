import json

with open('src/columns.json', encoding='utf-8') as file:
    COLUMNS = json.load(file)

COLUMNS.extend(['Año'])

with open('src/tables_to_update.json', encoding='utf-8') as file:
    TABLES_TO_UPDATE = json.load(file)
