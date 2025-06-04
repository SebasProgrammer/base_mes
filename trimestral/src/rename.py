import re
import argparse
from unicodedata import normalize

def normalize_name(name:str) -> str:
    new_name = re.sub(r'[%]','', name)
    new_name = re.sub(r'[%]','', new_name)
    new_name = re.sub(r'[/=]','',new_name)
    new_name = new_name.replace('(','').replace(')','').replace('.','').replace(',','').replace('-','')
    # Splits the string into a list of words
    word_list = new_name.split()  
    
    # If the string exceeds the sql character limit = 53, then we replace trivial words 
    if len("_".join(word_list)) > 53: 
        word_list = list(filter(lambda x: x != "de", word_list))
        word_list = list(filter(lambda x: x != "en", word_list))
        word_list = list(filter(lambda x: x != "del", word_list))
        word_list = list(filter(lambda x: x != "a", word_list))
        # In case there is a sql field name wich contains the word 'la" such as "La Libertad" then it deletes it, uncomment if there is no such case.
        #word_list = list(filter(lambda x: x != "la", word_list)) 
        concatenated_word = "_".join(word_list)
    else:
        concatenated_word = "_".join(word_list)  # Unir las word_list con guiones bajos
    return concatenated_word

def remove_tildes(s:str) -> str:
    '''
    source: https://es.stackoverflow.com/questions/135707/c%C3%B3mo-puedo-reemplazar-las-letras-con-tildes-por-las-mismas-sin-tilde-pero-no-l
    '''
    s = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", s), 0, re.I
    )

    # -> NFC
    s = normalize( 'NFC', s)

    return s.lower()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Tests renaming the variable name.')
    parser.add_argument('column', metavar='C', type=str, nargs=1,
                    help='column_name to rename')
    args = parser.parse_args()

    column = args.column[0]
    column_without_tildes = remove_tildes(column)
    column_sql = normalize_name(remove_tildes(column))
    print(f'Column read [{column}] \n\t Column SQL: [{column_sql}]')