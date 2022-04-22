import pyodbc
import pandas as pd
import os
import pdb

def generate_connection_cursor(is_mute_connection_print=True):
    """
    Connecting to database Cloudfm_IOT_Cody with username 'cody'.
    It will print out the server information if the connection is successful.
    """
    def _build_connection():
        
        server = os.environ['SQL_SERVER']
        database = os.environ['SQL_DATABASE'] # 
        uid = os.environ['SQL_UID']
        pwd = os.environ['SQL_PWD']
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                              SERVER=' + server + '; \
                              DATABASE=' + database + '; \
                              UID=' + uid + '; \
                              PWD=' + pwd)
        
        return cnxn
            
    cnxn = _build_connection()
    cursor = cnxn.cursor()
    
    if not is_mute_connection_print:
        test_connection(cursor)
    
    return cursor, cnxn

def query_data_from_sql(conn, 
                        table_name = 'tbl_Asset'):
    sql = """
    Select * from {table_name};""".format(table_name = table_name)
    
    df = pd.read_sql(sql, conn)
    return df

def write_records_to_sql(cursor, reader_export_to_sql, 
                         table_name = 'tbl_Asset',
                         table_columns = ['Action_Time',
                                            'time_of_day_in_float', 
                                            'Asset_Name',
                                            'Building_Name', 
                                            'Operation_Action', 
                                            'Client_Name',
                                            'clientId',
                                            'buildingId'],
                         chunk_row_size = 900):
    
    try:
        reader_export_to_sql.shape[1]
    except:
        reader_export_to_sql = reader_export_to_sql.to_frame().T
        
    number_rows = reader_export_to_sql.shape[0]
    
    chunk_row_size = min(chunk_row_size, 1000)
    
    for i in range(0, number_rows, chunk_row_size):
    
        rows=reader_export_to_sql.iloc[i:i+chunk_row_size].values

        # pdb.set_trace()
        
        insert_values = [tuple(row) for row in rows]
        table_columns_string = ', '.join(table_columns)
        table_name_and_columns = '{table_name} ({table_columns_string})'.format(table_name = table_name,
                                                                               table_columns_string=table_columns_string)

        cursor.execute(
            ' '.join([
                'insert into ',
                table_name_and_columns,
                'values',
                ','.join(
                    [str(i) for i in insert_values]
                )
            ])
        )

        cursor.commit()
        
    print(str(number_rows)+' new records have been saved to SQL "tbl_Asset" table!')
    
def write_record_to_sql_line_by_line(cursor, reader_export_to_sql):
    """
    The requirement for dataframe columns should be:
        Action_Time, 
        Asset_Name, 
        Building_Name, 
        Operation_Action, 
        Client_Name
    """
    
    try:
        reader_export_to_sql.shape[1]
    except:
        reader_export_to_sql = reader_export_to_sql.to_frame().T
        
    number_rows = reader_export_to_sql.shape[0]
    
    for _i, row in reader_export_to_sql.iterrows():
        sql = """INSERT INTO tbl_Asset (Action_Time, time_of_day_in_float, Asset_Name, Building_Name, Operation_Action, Client_Name) 
        VALUES (?, ?, ?, ?, ?)"""
        cursor.execute(sql, tuple(row))

        # the connection is not autocommitted by default, so we must commit to save our changes
        cursor.commit()
        
    print(str(number_rows)+' new records have been saved to SQL table!')  

def test_connection(cursor):
        """
        Sample select query
        """
        cursor.execute("SELECT @@version;") 
        row = cursor.fetchone() 
        while row: 
            print(row[0])
            row = cursor.fetchone()

def close_connection(cursor, cnxn, 
                     is_mute_connection_print=False):
    
    cursor.close()
    cnxn.close()
    
    if not is_mute_connection_print:
        return print('The SQL server connection has been closed.') 

def delete_records_in_sql(table_name = 'tbl_Asset', 
                          is_mute_connection_print=True):
    
    cursor, cnxn = generate_connection_cursor()
    
    # delete selected rows
    sql = """
            DELETE 
            FROM
                {table_name};""".format(table_name = table_name)
    cursor.execute(sql)

    # the connection is not autocommitted by default, so we must commit to save our changes
    cursor.commit()
    print('All records in SQL table {} have been deleted!'.format(table_name))
    close_connection(cursor, cnxn, is_mute_connection_print=is_mute_connection_print)
    
def write_suggested_time_to_sql(cursor, reader_export_to_sql, 
                                table_name = 'tbl_AssetSuggestedTime',
                                table_columns = ['clientId',
                                                 'Client_Name', 
                                                 'buildingId',
                                                 'Building_Name', 
                                                 'Asset_Name', 
                                                 'Day_Of_The_Week', 
                                                 'time_of_day_in_float', 
                                                 'Suggested_Time', 
                                                 'Operation_Action'],
                                chunk_row_size=900):

    try:
        reader_export_to_sql.shape[1]
    except:
        reader_export_to_sql = reader_export_to_sql.to_frame().T

    number_rows = reader_export_to_sql.shape[0]

    chunk_row_size = min(chunk_row_size, 1000)

    for i in range(0, number_rows, chunk_row_size):

        rows = reader_export_to_sql.iloc[i:i+chunk_row_size].values

        insert_values = [tuple(row) for row in rows]
        table_columns_string = ', '.join(table_columns)
        table_name_and_columns = '{table_name} ({table_columns_string})'.format(table_name = table_name,
                                                                                table_columns_string=table_columns_string)

        cursor.execute(
            ' '.join([
                'insert into ',
                table_name_and_columns,
                'values',
                ','.join(
                    [str(i) for i in insert_values]
                )
            ])
        )

        cursor.commit()

    print(str(number_rows)+' new records have been saved to SQL tbl_AssetSuggestedTime table!')
    
    