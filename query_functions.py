import pandas as pd  # import the data as dataframe and manipulate the data
from influxdb import InfluxDBClient
import numpy as np


def query_data(client,
               building_name = 'Braintree', 
               asset_name = 'Pizza Oven Top',
               start_date = '2019-07-01', 
               end_date = '2020-02-01',
               number_of_days = 10):

    df = pd.DataFrame()
    timestamp_start = pd.Timestamp(start_date)
    timestamp_end = pd.Timestamp(end_date)
    
    timestamp_duration =  timestamp_end - timestamp_start
    number_of_partition = np.ceil(timestamp_duration / pd.Timedelta(str(number_of_days) + ' days'))
    
    for date in pd.date_range(start=start_date, end=end_date, closed='right',periods=number_of_partition+1):
        timestamp_start_str = timestamp_start.strftime("%Y-%m-%d %H:%M:%S")
        timestamp_end_str = date.strftime("%Y-%m-%d %H:%M:%S")

        q = """SELECT hardwareid, time, value
               FROM "iotdata-dev" 
               WHERE (buildingName = $building_name AND assetProductCategory = $asset_name) 
               AND (time >= $start_time AND time < $end_time) tz('Europe/London')"""
        results = client.query(q, bind_params={'start_time': timestamp_start_str, 
                                               'end_time': timestamp_end_str,
                                               'building_name': building_name,
                                               'asset_name': asset_name})

        # dump the data to dataframe
        df_new = pd.DataFrame(results.get_points())
        # append the new record to the records list
        df = df.append(df_new, ignore_index=True)

        timestamp_start = date
    
    return df

def query_data_in_mins(client,
                        building_name = 'Braintree', 
                        asset_name = 'Pizza Oven Top',
                        start_date = '2019-07-01', 
                        end_date = '2020-02-01',
                        is_mute_print = False,
                        number_of_days = 10):

    df = pd.DataFrame()
    timestamp_start = pd.Timestamp(start_date)
    timestamp_end = pd.Timestamp(end_date)
    
    timestamp_duration =  timestamp_end - timestamp_start
    number_of_partition = np.ceil(timestamp_duration / pd.Timedelta(str(number_of_days) + ' days'))
    
    for date in pd.date_range(start=start_date, end=end_date, closed='right',periods=number_of_partition+1):
        timestamp_start_str = timestamp_start.strftime("%Y-%m-%d %H:%M:%S")
        timestamp_end_str = date.strftime("%Y-%m-%d %H:%M:%S")
        
        if not is_mute_print:
            print(timestamp_end_str)

        q = """SELECT mean(value) as value
               FROM "iotdata-dev" 
               WHERE (buildingName = $building_name AND assetProductCategory = $asset_name) 
               AND (time >= $start_time AND time < $end_time) 
               GROUP BY time(1m), "hardwareid" fill(previous)"""
        results = client.query(q, bind_params={'start_time': timestamp_start_str, 
                                               'end_time': timestamp_end_str,
                                               'building_name': building_name,
                                               'asset_name': asset_name})

        # dump the data to dataframe
        #df_new = pd.DataFrame(results.get_points(tags={'hardwareid': '1.1.55.2/analogue/0'}))
        # print(results.items())
        for key, generator in results.items():
            df_new = pd.DataFrame(generator)
            hardwareid = list(key[1].values())[0]
            if ('analogue' in hardwareid):
                df_new["hardwareid"] = hardwareid
                # print(list(key[1].values())[0], '\n')
                # append the new record to the records list
                df = df.append(df_new, ignore_index=True)

        timestamp_start = date
    # print(df.columns)
    # print(df.shape)
    
    if not df.shape[0]:
        df_avg = pd.DataFrame(columns=['time', 'no_of_ids', 'value']).set_index('time')
        df_avg.index = pd.to_datetime(df_avg.index).tz_localize('UTC').tz_convert('Europe/London')
        df_avg.no_of_ids = df_avg.no_of_ids.astype('int64')
        df_avg.value = df_avg.value.astype('float64')
    else:
        df_avg = df.groupby('time').mean()
        df_avg['no_of_ids'] = df["hardwareid"].nunique()
        
        df_avg.index = pd.to_datetime(df_avg.index)
        # converting timezone aware datetime format to naive datetime format
        df_avg.index = df_avg.index.tz_convert('Europe/London')
        
    return df_avg

def pivot_data(df, 
               columns='hardwareid', 
               index='time', 
               value='value'):
    
    # reshape the dataframe into pivot table
    df_pivot = df.pivot(columns=columns, index=index)[value]

    # converting Time from object type to datetime format
    df_pivot.index = pd.to_datetime(df_pivot.index)

    # converting timezone aware datetime format to naive datetime format
    # df_pivot.index = df_pivot.index.tz_convert('Europe/London')
    
    return df_pivot

def resample_data(df_pivot, 
                  interval='1Min', 
                  rule='1S'):

    df_pivot_resample = df_pivot.resample(rule= rule, fill_method='ffill', kind='timestamp', how='last')
    df_pivot_output = df_pivot_resample.resample(interval).mean()

    return df_pivot_output

def mean_data_columns(df_pivot_mins, 
                      column_name='current_avg_Amps'):
    
    return df_pivot_mins.T.mean().to_frame(name=column_name)

def pivot_resample_mean(df, 
                        columns='hardwareid', 
                        index='time', 
                        value='value', 
                        interval='1Min', 
                        rule='1S', 
                        column_name='current_avg_Amps'):
    
    df_pivot = pivot_data(df, columns=columns, index=index, value=value)
    df_pivot_mins = resample_data(df_pivot, interval=interval, rule=rule)
                                  
    return mean_data_columns(df_pivot_mins, column_name=column_name)

def query_data_in_mins_for_all_assets(client, asset_dict,
                                        building_name='Braintree',
                                        start_date='2019-07-01',
                                        end_date='2020-02-01',
                                        number_of_days=10,
                                        is_mute_print=False,
                                        name_of_asset_column='asset_name'):

    reader = pd.DataFrame()
    for asset in asset_dict:
        if not is_mute_print:
            print(building_name, '---', asset)
        reader_new = query_data_in_mins(client,
                                        building_name=building_name,
                                        asset_name=asset,
                                        start_date=start_date,
                                        end_date=end_date,
                                        is_mute_print=is_mute_print,
                                        number_of_days=number_of_days)
        reader_new[name_of_asset_column] = asset
        reader = reader.append(reader_new)
    
    return reader

def query_data_in_mins_for_all_building_assets(client, building_asset_dict, 
                                               start_date='2019-07-01',
                                               end_date='2020-02-01',
                                               number_of_days=10, 
                                               is_mute_print=False,
                                               name_of_building_column='building_name',
                                               name_of_asset_column='asset_name'):
    
    reader = pd.DataFrame()
    for restaurant in building_asset_dict:
        if not is_mute_print:
            print(restaurant)
        reader_new = query_data_in_mins_for_all_assets(client, building_asset_dict[restaurant], 
                                                        building_name=restaurant,
                                                        start_date=start_date,
                                                        end_date=end_date,
                                                        is_mute_print=is_mute_print,
                                                        number_of_days=number_of_days,
                                                        name_of_asset_column=name_of_asset_column)
        reader_new[name_of_building_column] = restaurant
        reader = reader.append(reader_new)
        
    return reader

def query_power_data_in_quarter(client,
                                building_name='Braintree',
                                start_date='2019-07-01',
                                end_date='2020-02-01'):

    timestamp_start_str = pd.Timestamp(
        start_date).strftime("%Y-%m-%d %H:%M:%S")
    timestamp_end_str = pd.Timestamp(end_date).strftime("%Y-%m-%d %H:%M:%S")

    q = """SELECT assetProductCategory, hardwareid, time, value
           FROM "iotdata-power" 
           WHERE (buildingName = $building_name) 
           AND (time >= $start_time AND time < $end_time)"""
    results = client.query(q, bind_params={'start_time': timestamp_start_str,
                                           'end_time': timestamp_end_str,
                                           'building_name': building_name})
    
    df = pd.DataFrame(results.get_points())
    df = df.groupby(['time', 'assetProductCategory'])['value'].sum().reset_index()
    
    df = df.rename(columns={'assetProductCategory': 'asset_name'})

    df.time = pd.to_datetime(df.time)
    df.time = df.time.dt.tz_convert('Europe/London')
    
    df.asset_name.fillna('Building', inplace=True)
    
    return df.set_index('time')