## Python packages installed

```
Office365_REST_Python_Client==2.5.5
pandas==2.2.2
psycopg2_binary==2.9.9
pyaml_env==1.2.1
python-dotenv==1.0.1
pytz==2024.1
SQLAlchemy==2.0.29
openpyxl==3.1.2
```

## Before building DOCKER

In case some anually variables are added and are not automatized then `column_names_json_creator.py` inside `annually/pre_docker_setup` folder should be ran to create new jsons. Inside `anually` we should run:

 - `python -m pre_docker_setup.colmn_names_json_creator`