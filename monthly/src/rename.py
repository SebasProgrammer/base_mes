import argparse
import re

def rename_mensual(col: str) -> str:
    '''
    Drops % symbols in the string, replaces /,= with _ and any double spaces '  ' or more with only one ' '.
    '''
    if col == 'Ventas de empresas de manufactura de alimentos y bebidas (var. % nominal)':
        return 'ventas_empresas_manufactura_alimentos_y_bebidas_var_nominal'

    new_col = re.sub(r'[%]','',col)
    new_col = re.sub(r'[/=]','_',new_col)
    new_col = re.sub(r"\s+", ' ' , new_col).strip()
        
    if len(new_col) >= 63:
        return new_col[:63]
    else:
        return new_col


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Tests renaming the variable name.')
    parser.add_argument('column', metavar='C', type=str, nargs=1,
                    help='column_name to rename')
    args = parser.parse_args()

    column = args.column[0]
    column_sql = rename_mensual(column)
    print(f'Column read [{column}] \n\t Column SQL: [{column_sql}]')
