# queryeasy
Execute SQL queries on data present in CSV or Excel files. Also allows to generate the query output files.

## Features

- Query the CSV or Excel files using sql queries
- Provides the option to store the query output to .xls, .xlsx, .csv formats
- Formats the output to fit in the terminal 
- Removes the spaces from the column headers to ease query process
- Saves the output file to default dir if no path is specified



## Installation

You can pip install the package using

```sh
pip install queryeasy
```

The command line utility will be installed as 
queryeasy to bin on Linux (e.g. /usr/bin); or as
queryeasy.exe to Scripts in your Python installation on Windows 
(e.g. C:\Python3\Scripts\tabulate.exe).


After installing, check the version

```sh
queryeasy --version
```

## Usage

#### queryeasy [-h] [-s sheet_name] [-o output_file] [-v] filename sql_query

It can be used to execute sql queries on csv file

```shell
queryeasy sample.csv "select * from sample"
```

It can be used to execute sql queries on excel file
```shell
queryeasy sample.xls "select * from sample" -s Sheet1
queryeasy sample.xlsx "select * from sample" -s Sheet3
```

The output of the performed query can be saved to a csv or excel file

```shell
queryeasy sample.xls "select * from sample" -s Sheet1 -o /path/output.xls
queryeasy sample.xlsx "select * from sample" -s Sheet3 -o /path/output.xlsx
queryeasy sample.xlsx "select * from sample" -s Sheet3 -o output.xlsx
queryeasy sample.csv "select * from sample" -s Sheet3 -o /path/output.csv
queryeasy sample.csv "select * from sample" -s Sheet3 -o output
```

## Arguments
<pre>
positional arguments: 
  filename              Enter the file path/name
  sql_query             Enter the SQL query

optional arguments:
  -h, --help            show this help message and exit
  -s sheet_name, --sheet sheet_name
                        Provide the sheet name for excel file
  -o output_file, --output output_file
                        Output file path/name to store results
  -v, --version         show program's version number and exit
</pre>

## Notes
- Table names used in the SQL query should match the input CSV/Excel file names,
      without the ".csv" or ".xls" extension
- While entering query, replace the spaces in column names with underscore(_)
- The default output file extension is .csv
- The output file supports ".xlsx", ".xls", ".csv" extensions as of now

## Contribute

The library is in initial stage and requires a lot of work, please feel free to contribute
