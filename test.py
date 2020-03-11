
import pandas as pd # import the data as dataframe and manipulate the data
from influxdb import InfluxDBClient
import time
import os
import sys

from sql_functions import delete_records_in_sql

from processing_functions import (init_building_asset_dict,
                                          init_assets_current_time_margins,
                                          source_to_label_range_shift)

from dependent_functions import (initialize_data,
                                   update_data,
                                   save_on_off_action_records_to_sql,
                                   update_suggested_time_in_sql)

print('Hello!')

os.environ['InfluxDB_HOST']="40.127.129.239"
os.environ['InfluxDB_PORT']="8086"
os.environ['InfluxDB_DATABASE']="iot"

os.environ['SQL_SERVER']="10.0.1.8\\TEST2017"
os.environ['SQL_DATABASE']="Cloudfm_IOT_Cody"
os.environ['SQL_UID']="cody"
os.environ['SQL_PWD']="jiuren"

building_asset_dict = init_building_asset_dict()
assets_current_time_margins_dict = init_assets_current_time_margins()
margin_period = '5 hours'
loop_count = 0

try:
    mode = sys.argv[1]
except:
    print('The working mode variable is needed. "i" for initialization, "r" for recovering.')    

if mode == "r":
    
    print('About to read data from pickle ...')
    try:
        reader = pd.read_pickle('reader.pkl') 
        print('Read data from pickle ...')
        end_time = reader.index.tz_convert(None).max() + pd.Timedelta('1 min')
        print('Recovering from before ...')
    except:
        print('I cannot find the reader.pkl file.')
        quit()
    
else:
    
    print('Starting from the very beginning ...')
    
    if mode == 't':
        start_time = '2020-03-01'
    elif mode == 'i':
        start_time = '2019-07-01'
        
    end_time = '2020-03-02'

    reader, start_time, end_time = initialize_data(building_asset_dict,
                                                is_mute_print=False,
                                                start_time=start_time,
                                                end_time=end_time)

    # delete_records_in_sql()

    label_time_start, label_time_end = source_to_label_range_shift(
        start_time, end_time, margin_period, is_initial=True)

    # has_new_records = save_on_off_action_records_to_sql(reader, assets_current_time_margins_dict,
    #                                 start_time=label_time_start,
    #                                 end_time=label_time_end,
    #                                 is_mute_print = False,
    #                                 margin_period=margin_period)
    # if has_new_records:
    #     update_suggested_time_in_sql(suggested_percentile=50)
    
    reader.to_pickle('reader.pkl')
    
while True:
    
    if pd.Timestamp.now().floor('min') - end_time > pd.Timedelta('60 min'):
        
        print('Data in both tbl_Asset and tbl_AssetSuggestedTime tables is being updated ...')
        reader, start_time, end_time = update_data(reader, building_asset_dict, 
                                                   retention_period = '10 days',
                                                   is_mute_print = True)

        label_time_start, label_time_end = source_to_label_range_shift(
            start_time, end_time, margin_period)

        # has_new_records = save_on_off_action_records_to_sql(reader, assets_current_time_margins_dict,
        #                                   start_time=label_time_start,
        #                                   end_time=label_time_end,
        #                                   margin_period=margin_period)
        # if has_new_records:
        #     update_suggested_time_in_sql(suggested_percentile=50)
        
        reader.to_pickle('reader.pkl')
        loop_count = 0
        print('reader.index.min()', reader.index.min())
        print('reader.index.max()', reader.index.max())
        print('label_time_start', label_time_start)
        print('label_time_end', label_time_end)
        print('Data in both tables has been updated!')
        print('Current time:', pd.Timestamp.now().floor('min'))
    
    loop_count = loop_count+1    
    print('Data is up-to-date!', 'Loop count:', loop_count)
    time.sleep(5)

