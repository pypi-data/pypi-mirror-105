# Time    : 08/05/21
# Author  : Dheeraj Alimchandani
# Email   : dheeraj.alim@gmail.com

import os
import argparse
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy import create_engine
import pandas as pd
import time
import uuid
from functools import reduce

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

VERSION = "queryeasy 0.0.1"
__help_msg = """
Copyright (c) 2021, Dheeraj Alimchandani, MIT License
dheeraj.alim@gmail.com
More at : https://github.com/dheerajalim/queryeasy
Syntax:
    queryeasy [options] <SQL QUERY>

Notes:
   1. Table names used in the SQL should match the input CSV/Excel file names,
      without the ".csv" or ".xls" extension
   2. While entering query, replace the spaces in column names with underscore(_)
   3. The default output file extension is .csv
   4. The output file supports ".xlsx", ".xls", ".csv" extensions as of now

"""


def __argument_parser():
    parser = argparse.ArgumentParser(prog='queryeasy', description=__help_msg,
                                     epilog='Enjoy Querying!', formatter_class=argparse.RawTextHelpFormatter)
    parser.version = VERSION

    # parser.add_argument("filename", help="Enter the file path/name", metavar="filename", nargs='+')
    parser.add_argument("filename", help="Enter the file path/name", metavar="filename")
    parser.add_argument("query", help="Enter the SQL query", metavar="sql_query")
    parser.add_argument("-s", "--sheet", help="Provide the sheet name for excel file", metavar="sheet_name")
    parser.add_argument("-o", "--output", help="Output file path/name to store results", metavar="output_file")
    parser.add_argument('-v', '--version', action='version')

    args = parser.parse_args()

    return args


def _file_details(file):
    _, filename = os.path.split(file)
    table_name, file_type = os.path.splitext(filename)

    if file_type not in [".xlsx", ".xls", ".csv"]:
        raise Exception("queryeasy currently supports only .xlsx, .xls, .csv file types")

    return table_name, file_type


def _output_file_details(file):
    filepath, filename = os.path.split(file)
    output_file_name, file_type = os.path.splitext(filename)

    if not filepath:
        filepath = os.path.abspath(os.getcwd())

    if filename:
        if filename[0] == '.' or output_file_name[0] == '.':
            if len(filename) == 1 or len(output_file_name) == 1:
                output_file_name = str(uuid.uuid4())
            else:
                output_file_name = output_file_name[1:]

    if not filename or not output_file_name:
        output_file_name = str(uuid.uuid4())

    if not file_type:
        file_type = '.csv'  # default type is .csv if none is specified

    if file_type not in [".xlsx", ".xls", ".csv"]:
        file_type = '.csv'

    output_file = filepath + '/' + output_file_name + file_type

    return output_file, file_type


def _generate_output_file(file, query_results):
    output_file, file_type = _output_file_details(file)

    if file_type == ".csv":
        query_results.to_csv(output_file, index=False)
        print(f'Output file generated : {str(output_file)}')
    elif file_type in [".xlsx", ".xls"]:
        query_results.to_excel(output_file, index=False)
        print(f'Output file generated : {str(output_file)}')
    else:
        raise Exception(f'Unable to create output file for {str(output_file)}{str(file_type)}')


def _execute_query(args):
    # fetching the name of the file
    file = args.filename
    # fetching the query to be executed
    query = args.query

    # getting file name and file type
    table_name, file_type = _file_details(file)

    # create sqlite engine
    engine = create_engine('sqlite://', echo=False)

    if file_type == ".csv":
        table = pd.read_csv(file)

    elif file_type in [".xlsx", ".xls"]:
        if args.sheet:
            table = pd.read_excel(file, sheet_name=args.sheet)
        else:
            raise Exception("For excel file , sheet name is mandatory")

    # replacing the space from column names with _
    table.columns = table.columns.str.replace(' ', '_')
    table.to_sql(table_name, engine, if_exists='replace', index=False)

    try:
        query_start_time = time.time()
        query_results = engine.execute(query)
        query_end_time = '{:.4f}'.format(time.time() - query_start_time)
        query_results = pd.DataFrame(query_results, columns=[col for col in query_results.keys()])

    except sqlalchemy.exc.OperationalError as query_exception:
        raise Exception(str(query_exception))

    except sqlalchemy.exc.SQLAlchemyError as query_exception:
        raise Exception(str(query_exception))

    return query_results, query_end_time


"""pp() function by Aaron Watters, posted to gadfly-rdbms@egroups.com 1999-01-18
# modified version
# Taken from sqliteplus.py by Florent Xicluna
"""


def _print_query_output(query_results, query_execution_time):
    headers = [col for col in query_results.columns]
    rows = query_results.values
    num_cols = range(len(headers))
    num_rows = range(len(rows))

    max_len_col = [max(0, len(headers[j]), *(len(str(rows[i][j])) for i in num_rows)) for j in num_cols]

    names = ' ' + ' | '.join(
        [headers[j].ljust(max_len_col[j]) for j in num_cols])
    sep = '=' * (reduce(lambda x, y: x + y, max_len_col) + 3 * len(headers) - 1)
    rows = [names, sep] + [' ' + ' | '.join(
        [str(rows[i][j]).ljust(max_len_col[j])
         for j in num_cols]) for i in num_rows]
    print('\n'.join(rows) + (
            len(rows) == 2 and '\n No Records Found\n' or '\n'))

    print(f'Query executed in : {str(query_execution_time)} secs')
    print(f'Total rows returned : {str(len(query_results.index))}')


def _run_query():
    try:
        # getting all the parameters
        args = __argument_parser()
        query_results, query_execution_time = _execute_query(args)
        if args.output:
            _generate_output_file(args.output, query_results)
        _print_query_output(query_results, query_execution_time)
        return
    except Exception as exception:
        print(str(exception))


if __name__ == "__main__":

    _run_query()

