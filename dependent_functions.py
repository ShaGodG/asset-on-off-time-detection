
import pandas as pd # import the data as dataframe and manipulate the data
from influxdb import InfluxDBClient
import time
import os
import pdb

from query_functions import (query_data_in_mins, 
                             query_data_in_mins_for_all_assets,
                             query_data_in_mins_for_all_building_assets)

from processing_functions import (init_building_asset_dict,
                                          init_assets_current_time_margins,
                                          init_assets_3d_plot_good_view,
                                          translate_asset_name,
                                          source_to_label_range_shift,
                                          label_on_off_status,
                                          label_on_off_status_for_all_building_assets,
                                          collect_on_off_action_records,
                                          generate_suggested_time,
                                          enrich_energy_cost_schema,
                                          enrich_time_schema)

from sql_functions import (generate_connection_cursor,
                           query_data_from_sql,
                                   write_record_to_sql_line_by_line,
                                   delete_records_in_sql,
                                   write_records_to_sql, 
                                   write_suggested_time_to_sql,
                                   close_connection)


def initialize_data(building_asset_dict, 
                    is_mute_print=False,
                    start_time='2019-07-01', 
                    end_time='2020-03-01'):

    client = InfluxDBClient(host=str(os.environ['InfluxDB_HOST']), 
                            port=int(os.environ['InfluxDB_PORT']), 
                            database=str(os.environ['InfluxDB_DATABASE']))
    reader = query_data_in_mins_for_all_building_assets(
        client, building_asset_dict, is_mute_print=is_mute_print, start_date=start_time, end_date=end_time)
    
    return reader, pd.Timestamp(start_time), pd.Timestamp(end_time)

def update_data(reader, building_asset_dict,
                is_mute_print=False,
                specified_time=False,
                retention_period=False,
                name_of_asset_column='asset_name',
                name_of_building_column='building_name'):

    if not specified_time:
        current_committe_time = pd.Timestamp.now().floor('min')
    else:
        current_committe_time = pd.Timestamp(specified_time)

    last_committe_time = (reader.index.tz_convert(
        None).max()+pd.Timedelta('1 min'))

    time_range_start = last_committe_time
    time_range_end = current_committe_time

    client = InfluxDBClient(host=str(os.environ['InfluxDB_HOST']), 
                            port=int(os.environ['InfluxDB_PORT']), 
                            database=str(os.environ['InfluxDB_DATABASE']))
    reader_new = query_data_in_mins_for_all_building_assets(client, building_asset_dict,
                                                            is_mute_print=is_mute_print,
                                                            start_date=last_committe_time,
                                                            end_date=current_committe_time,
                                                            name_of_building_column=name_of_building_column,
                                                            name_of_asset_column=name_of_asset_column)

    if retention_period:
        reader = reader.loc[reader.index.tz_convert(
            None) >= last_committe_time-pd.Timedelta(retention_period)]

    reader_appended_without_duplicate = reader.append(reader_new).reset_index().drop_duplicates(
        subset=['building_name', 'asset_name', 'time'], keep='first').set_index('time')

    reader_appended_without_duplicate_or_gap = reader_appended_without_duplicate.groupby(
        ['asset_name', 'building_name']).ffill()

    return reader_appended_without_duplicate_or_gap, time_range_start, time_range_end

def update_suggested_time_in_sql(suggested_percentile=50, 
                                 is_mute_connection_print=False):
    
    cursor, cnxn = generate_connection_cursor(is_mute_connection_print=is_mute_connection_print)
    
    # get the suggested time based on existing records
    df = query_data_from_sql(cnxn, table_name = 'tbl_Asset')
    
    if not df.shape[0]:
        
        print('The source table "tbl_Asset" is empty!')
        print('Please restart the service!')
    
    else:
        
        # pdb.set_trace()
        df_enriched_time = enrich_time_schema(df.set_index('Action_Time'))
        df_enriched_time['day_of_week'] = (df_enriched_time['day_of_week']+1)%7+1
        df_with_suggested_time = generate_suggested_time(df_enriched_time, 
                                                        suggested_percentile=suggested_percentile)
        
        delete_records_in_sql(table_name = 'tbl_AssetSuggestedTime')
        write_suggested_time_to_sql(cursor, df_with_suggested_time)
    
    close_connection(cursor, cnxn, is_mute_connection_print=is_mute_connection_print)

def save_on_off_action_records_to_sql(reader, assets_current_time_margins, id_dict,
                                      is_mute_print=False,
                                      start_time='2019-07-26',
                                      end_time='2019-07-28',
                                      margin_period='5 hours'):
    
    df_on_off_actions, _ = collect_on_off_action_records(reader, assets_current_time_margins,
                                                         start_time=start_time,
                                                         end_time=end_time,
                                                         margin_period=margin_period,
                                                         is_mute_print=is_mute_print)
    
    #print(df_on_off_actions)
    
    if df_on_off_actions.shape[0]:
    #if True:
        
        df_on_off_actions_for_export = transform_df_for_export(df_on_off_actions, id_dict)
        cursor, cnxn = generate_connection_cursor()
        write_records_to_sql(cursor, df_on_off_actions_for_export)
        close_connection(cursor, cnxn)
        
        return True
        
    else:
        
        print('No new record has to be saved to SQL table! So I did not access the SQL database.')
        
        return False
    
def transform_df_for_export(reader_with_on_off, id_dict,
                            select_existing_columns=['time',
                                                     'time_of_day_in_float',
                                                     'asset_name',
                                                     'building_name',
                                                     'on_off_action'],
                            new_columns_values_pairs={'client_name': 'Pizza Express'}):

    reader_with_on_off_and_time_in_float = enrich_time_schema(reader_with_on_off)
    reader_export_to_sql = reader_with_on_off_and_time_in_float.reset_index()[
        select_existing_columns]
    reader_export_to_sql = reader_export_to_sql.loc[(
        reader_export_to_sql.on_off_action == 1) | (reader_export_to_sql.on_off_action == -1)]
    reader_export_to_sql.on_off_action = (
        reader_export_to_sql.on_off_action + 1).div(2)
    reader_export_to_sql.time = reader_export_to_sql.time.dt.strftime(
        "%Y-%d-%m %H:%M:%S")
    
    for new_column in new_columns_values_pairs:
        reader_export_to_sql[new_column] = new_columns_values_pairs[new_column]
        
    # pdb.set_trace()
    
    # add client id
    reader_export_to_sql['client_id'] = reader_export_to_sql['client_name'].apply(lambda x: id_dict['client_id'][x])
    
    # add building id
    reader_export_to_sql['building_id'] = reader_export_to_sql['building_name'].apply(lambda x: id_dict['building_id'][x])

    return reader_export_to_sql

    