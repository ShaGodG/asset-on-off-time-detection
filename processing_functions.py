
import pandas as pd # import the data as dataframe and manipulate the data
import calendar
import datetime # to create data-time variables
import pdb

def init_building_asset_dict():

    building_asset_dict = {}

    building_asset_dict['Braintree'] = {'Air Conditioning': 'Air conditioning',
                                        'Dishwasher': 'Dishwasher',
                                        'Extraction Hood': 'Extraction hood',
                                        'Glass Washer': 'Glass washer',
                                        'Hot Water Cylinder': 'Mega-flo water tank',
                                        'Triple Deck Oven': 'Pizza oven',
                                        'Walk in Fridge': 'Walk in fridge',
                                        'Walk in Freezer': 'Walk in freezer'}

    building_asset_dict['Langham Place'] = {'Air Conditioning': 'Air conditioning',
                                            'Dishwasher': 'Dishwasher',
                                            'Extraction Hood': 'Extraction hood',
                                            'Glass Washer': 'Glass washer',
                                            'Hot Water Cylinder': 'Mega-flo water tank',
                                            'Triple Deck Oven': 'Pizza oven',
                                            'Walk in Fridge': 'Walk in fridge',
                                            'Walk in Freezer': 'Walk in freezer'}

    building_asset_dict['Uxbridge'] = {'HVAC': 'Air conditioning',
                                       'Dishwasher': 'Dishwasher',
                                       'Glass Washer': 'Glass washer',
                                       'Hot Water Cylinder': 'Mega-flo water tank',
                                       'Triple Deck Oven': 'Pizza oven',
                                       'Walk in Fridge': 'Walk in fridge',
                                       'Walk in Freezer': 'Walk in freezer'}

    return building_asset_dict

def init_assets_current_time_margins():

    assets_current_time_margins = {}

    assets_current_time_margins['Braintree'] = {#'Air Conditioning': {'current_value_margin': 1.5,
                                                #                     'expiration_time_margins': [20, 130]},
                                        'Dishwasher':  {'current_value_margin': 0.5,
                                                                     'expiration_time_margins': [20, 130]},
                                        'Extraction Hood':  {'current_value_margin': 0.2,
                                                                     'expiration_time_margins': [20, 130]},
                                        'Glass Washer':  {'current_value_margin': 0.5,
                                                                     'expiration_time_margins': [20, 130]},
                                        #'Hot Water Cylinder':  {'current_value_margin': 0.5,
                                        #                             'expiration_time_margins': [20, 130]},
                                        'Triple Deck Oven':  {'current_value_margin': 1,
                                                                     'expiration_time_margins': [20, 240]}}

    assets_current_time_margins['Langham Place'] = {#'Air Conditioning':  {'current_value_margin': 0.7,
                                                    #                 'expiration_time_margins': [20, 130]},
                                            'Dishwasher':  {'current_value_margin': 0.5,
                                                                     'expiration_time_margins': [20, 130]},
                                            'Extraction Hood':  {'current_value_margin': 0.5,
                                                                     'expiration_time_margins': [20, 130]},
                                            'Glass Washer':  {'current_value_margin': 0.7,
                                                                     'expiration_time_margins': [20, 130]},
                                            #'Hot Water Cylinder':  {'current_value_margin': 1.7,
                                            #                         'expiration_time_margins': [20, 130]},
                                            'Triple Deck Oven':  {'current_value_margin': 1,
                                                                     'expiration_time_margins': [20, 240]}}

    assets_current_time_margins['Uxbridge'] = {#'HVAC':  {'current_value_margin': 0.5,
                                               #                      'expiration_time_margins': [20, 130]},
                                                'Dishwasher':  {'current_value_margin': 0.5,
                                                                                'expiration_time_margins': [20, 230]},
                                                'Glass Washer':  {'current_value_margin': 0.5,
                                                                                'expiration_time_margins': [20, 130]},
                                                #'Hot Water Cylinder':  {'current_value_margin': 0.5,
                                                #                              'expiration_time_margins': [20, 130]},
                                                'Triple Deck Oven':  {'current_value_margin': 1,
                                                                                'expiration_time_margins': [20, 240]}}

    return assets_current_time_margins

def init_assets_3d_plot_good_view(restaurant):
    
    assets_3d_plot_good_view = {}
    
    assets_3d_plot_good_view['Braintree'] = {'Air conditioning': {'elev':34, 
                                                 'azim':-30,
                                                 'zlim3d': 50,
                                                 'ot_hms_ls': [0, 0, 0],
                                                 'ct_hms_ls': [23, 59, 59]},
                                  'Dishwasher': {'elev':39, 
                                                 'azim':-40,
                                                 'zlim3d': 60, 
                                                 'ot_hms_ls': [8, 30, 0], 
                                                 'ct_hms_ls': [10, 30, 0]},
                                  'Glass washer': {'elev':39, 
                                                 'azim':-40,
                                                 'zlim3d': 60, 
                                                 'ot_hms_ls': [8, 30, 0], 
                                                 'ct_hms_ls': [10, 30, 0]},
                                  'Extraction hood': {'elev':39, 
                                                      'azim':-50,
                                                      'zlim3d': 10, 
                                                      'ot_hms_ls': [0, 0, 0], 
                                                      'ct_hms_ls': [23, 59, 59]}, 
                                  'Pizza oven': {'elev':42, 
                                                 'azim':-33, 
                                                 'avg_elev':51, 
                                                 'avg_azim':-47,
                                                 'zlim3d': 100, 
                                                 'ot_hms_ls': [10, 0, 0],
                                                 'ct_hms_ls': [11, 30, 0]},
                                  'Walk in fridge': {'elev':39, 
                                                     'azim':-58,
                                                     'zlim3d': 17, 
                                                     'ot_hms_ls': [0, 0, 0],
                                                     'ct_hms_ls': [23, 59, 59]},
                                'Mega-flo water tank': {'elev':39, 
                                                     'azim':-58,
                                                     'zlim3d': 50, 
                                                     'ot_hms_ls': [0, 0, 0],
                                                     'ct_hms_ls': [23, 59, 59]}, 
                                  'Walk in freezer': {'elev':54, 
                                                      'azim':-51,
                                                      'zlim3d': 30, 
                                                      'ot_hms_ls': [0, 0, 0], 
                                                      'ct_hms_ls': [23, 59, 59]}}
    
    assets_3d_plot_good_view['Langham Place'] = {'Air conditioning': {'elev': 34,
                                                 'azim': -30,
                                                 'zlim3d': 30,
                                                 'ot_hms_ls': [0, 0, 0],
                                                 'ct_hms_ls': [23, 59, 59]},
                            'Dishwasher': {'elev': 39,
                                           'azim': -40,
                                           'zlim3d': 60,
                                           'ot_hms_ls': [8, 30, 0],
                                           'ct_hms_ls': [10, 30, 0]},
                            'Glass washer': {'elev': 39,
                                             'azim': -40,
                                             'zlim3d': 23,
                                             'ot_hms_ls': [8, 30, 0],
                                             'ct_hms_ls': [17, 30, 0]},
                            'Extraction hood': {'elev': 39,
                                                'azim': -50,
                                                'zlim3d': 10,
                                                'ot_hms_ls': [0, 0, 0],
                                                'ct_hms_ls': [23, 59, 59]},
                            'Pizza oven': {'elev': 42,
                                           'azim': -33,
                                           'avg_elev': 51,
                                           'avg_azim': -47,
                                           'zlim3d': 100,
                                           'ot_hms_ls': [10, 0, 0],
                                           'ct_hms_ls': [11, 30, 0]},
                            'Walk in fridge': {'elev': 39,
                                               'azim': -58,
                                               'zlim3d': 17,
                                               'ot_hms_ls': [0, 0, 0],
                                               'ct_hms_ls': [23, 59, 59]},
                            'Mega-flo water tank': {'elev': 34,
                                                    'azim': -40,
                                                    'zlim3d': 7,
                                                    'ot_hms_ls': [0, 0, 0],
                                                    'ct_hms_ls': [23, 59, 59]},
                            'Walk in freezer': {'elev': 40,
                                                'azim': -46,
                                                'zlim3d': 30,
                                                'ot_hms_ls': [0, 0, 0],
                                                'ct_hms_ls': [23, 59, 59]}}
    
    assets_3d_plot_good_view['Uxbridge'] = {'Air conditioning': {'elev': 34,
                                                 'azim': -30,
                                                 'zlim3d': 3,
                                                 'ot_hms_ls': [0, 0, 0],
                                                 'ct_hms_ls': [23, 59, 59]},
                                            'Dishwasher': {'elev': 50,
                                                            'azim': -47,
                                                            'zlim3d': 40,
                                                            'ot_hms_ls': [8, 30, 0],
                                                            'ct_hms_ls': [10, 30, 0]},
                                            'Glass washer': {'elev': 39,
                                                                'azim': -40,
                                                                'zlim3d': 23,
                                                                'ot_hms_ls': [8, 30, 0],
                                                                'ct_hms_ls': [17, 30, 0]},
                                            'Pizza oven': {'elev': 50,
                                                            'azim': -58,
                                                            'avg_elev': 51,
                                                            'avg_azim': -47,
                                                            'zlim3d': 70,
                                                            'ot_hms_ls': [10, 0, 0],
                                                            'ct_hms_ls': [11, 30, 0]},
                                            'Walk in fridge': {'elev': 39,
                                                                'azim': -58,
                                                                'zlim3d': 17,
                                                                'ot_hms_ls': [0, 0, 0],
                                                                'ct_hms_ls': [23, 59, 59]},
                                            'Mega-flo water tank': {'elev': 34,
                                                                    'azim': -40,
                                                                    'zlim3d': 7,
                                                                    'ot_hms_ls': [0, 0, 0],
                                                                    'ct_hms_ls': [23, 59, 59]},
                                            'Walk in freezer': {'elev': 57,
                                                                'azim': -40,
                                                                'zlim3d': 60,
                                                                'ot_hms_ls': [0, 0, 0],
                                                                'ct_hms_ls': [23, 59, 59]}}

    return assets_3d_plot_good_view[restaurant]

def init_id_dict():
    
    id_dict = {}
    
    id_dict['building_id'] = {}
    id_dict['building_id']['Braintree'] = 64
    id_dict['building_id']['Langham Place'] = 251
    id_dict['building_id']['Uxbridge'] = 436
    
    id_dict['client_id'] = {}
    id_dict['client_id']['Pizza Express'] = 1
    id_dict['client_id']['KFC'] = 2
    
    return id_dict

def time_format_func(value): # time format function used in the yaxis ticklabel in the boxplot
    
    # find numbers for hour, minute, second 
    value_in_seconds = int(value*3600)
    minute_value, second_value = divmod(value_in_seconds, 60)
    hour_value, minute_value = divmod(minute_value, 60)
    hour_value = hour_value % 24
    #print(hour_value)
    
    return datetime.time(hour_value, minute_value, second_value)

def translate_asset_name(reader, assets_series_to_name_dict, 
                         asset_name='asset_name'):
    reader['refined_asset_name'] = reader[asset_name].apply(lambda series: assets_series_to_name_dict[series])
    return reader

def enrich_energy_cost_schema(df_pivot_mins, 
                              current_avg_Amps='value', 
                              number_of_phases='no_of_ids',
                              electricity_price = 0.148, # pounds per kWh
                              single_phase_voltage = 230, # v, equivalently 230 v for single phase
                              minute_to_hour = 1/60,
                              power_factor = 1):

    # calculate the energy consumption

    df_pivot_mins['energy_value_kWh'] = (df_pivot_mins[current_avg_Amps]*df_pivot_mins[number_of_phases]).apply(lambda current: current*single_phase_voltage*power_factor*minute_to_hour/1000)
    
    #.apply(lambda current: current*single_phase_voltage*power_factor*minute_to_hour/1000) # kWh
    df_pivot_mins['cost_value_£'] = df_pivot_mins['energy_value_kWh'].apply(
        lambda energy: energy*electricity_price) # £ pounds
    
    return df_pivot_mins

def enrich_time_schema(df_pivot_resample):
    
    # create columns for date and time
    df_pivot_resample['time_of_day'] = df_pivot_resample.index.time
    df_pivot_resample['time_of_day_in_float'] = df_pivot_resample['time_of_day'].apply(lambda x: x.hour+x.minute/60+x.second/3600)
    df_pivot_resample['hour_of_day'] =  df_pivot_resample.index.hour
    df_pivot_resample['date'] = df_pivot_resample.index.date
    df_pivot_resample['day_of_month'] = df_pivot_resample.index.day
    df_pivot_resample['day_of_year'] = df_pivot_resample.index.dayofyear
    df_pivot_resample['week_of_year'] = df_pivot_resample.index.weekofyear
    df_pivot_resample['day_of_week'] = df_pivot_resample.index.weekday
    df_pivot_resample['day_of_week_name'] = df_pivot_resample['day_of_week'].apply(lambda x: str(calendar.day_name[x]))
    df_pivot_resample['day_of_week_abbr_name'] = df_pivot_resample['day_of_week'].apply(lambda x: str(calendar.day_abbr[x]))

    return df_pivot_resample # timestamp as index

def label_on_off_status(df_pivot_resample, 
                        column_name='value',
                        current_value_margin = 1, # in Amps
                        expiration_time_margins = [20, 240], # in minutes
                        ):

    df_pivot_resample['on_off_temp_status'] = df_pivot_resample[column_name].gt(current_value_margin).astype('int32')
    df_pivot_resample['on_off_perm_status'] = df_pivot_resample['on_off_temp_status'].rolling(expiration_time_margins[1]).max().shift(1-expiration_time_margins[1]).rolling(expiration_time_margins[1]).min()
    df_pivot_resample['on_off_perm_status_refined'] = df_pivot_resample['on_off_perm_status'].rolling(expiration_time_margins[0]).min().shift(1-expiration_time_margins[0]).rolling(expiration_time_margins[0]).max()
    df_pivot_resample['on_off_action'] = df_pivot_resample['on_off_perm_status_refined'].diff()
    
    return df_pivot_resample

def init_label_on_off_status_for_all_building_assets(reader, assets_current_time_margins,
                                                     assets_saved_state = {},
                                                     column_name='value',
                                                     building_name = 'building_name',
                                                     asset_name = 'asset_name'
                                                     ):
    
    reader_with_on_off = pd.DataFrame()
    
    for building in assets_current_time_margins:
        
        print(building)
        assets_saved_state[building] = {}

        for asset in assets_current_time_margins[building]:
            print('---', asset)
            reader_selected_asset = reader.loc[(
                reader[building_name] == building) & (reader[asset_name] == asset)]
            reader_selected_asset.ffill(axis=0, inplace=True)
            assets_saved_state[building][asset] = reader_selected_asset.tail(1)
            reader_selected_asset_with_on_off = label_on_off_status(reader_selected_asset,
                                                                    column_name = column_name,
                                                                    expiration_time_margins = assets_current_time_margins[
                                                                        building][asset]['expiration_time_margins'],
                                                                    current_value_margin = assets_current_time_margins[building][asset]['current_value_margin'])
            # print(reader_selected_asset_with_on_off.shape)
            reader_with_on_off = reader_with_on_off.append(
                reader_selected_asset_with_on_off)
            
    return reader_with_on_off, assets_saved_state

def label_on_off_status_for_all_building_assets(reader, assets_current_time_margins, 
                                                column_name='value',
                                                building_column_name = 'building_name',
                                                asset_column_name = 'asset_name',
                                                is_mute_print = False
                                                ):
    
    reader_with_on_off = pd.DataFrame()
    
    for building in assets_current_time_margins:
        
        if not is_mute_print:
            print(building)

        for asset in assets_current_time_margins[building]:
            
            if not is_mute_print:
                print('---', asset)
                
            reader_selected_asset = reader.loc[(
                reader[building_column_name] == building) & (reader[asset_column_name] == asset)]
            
            # if assets_saved_state:
            #     reader_selected_asset = assets_saved_state[building][asset].append(reader_selected_asset)
            # else:
            #     assets_saved_state = assets_saved_state.update()
                
            reader_selected_asset.ffill(axis = 0, inplace=True)
            # assets_saved_state[building][asset] = reader_selected_asset.tail(1)
            reader_selected_asset_with_on_off = label_on_off_status(reader_selected_asset,
                                                                    column_name = column_name,
                                                                    expiration_time_margins = assets_current_time_margins[
                                                                        building][asset]['expiration_time_margins'],
                                                                    current_value_margin = assets_current_time_margins[building][asset]['current_value_margin'])
            if not is_mute_print:
                print(reader_selected_asset_with_on_off.shape)
            reader_with_on_off = reader_with_on_off.append(reader_selected_asset_with_on_off)
        
    return reader_with_on_off

def collect_on_off_action_records(df, assets_current_time_margins, 
                                   time_column=False, 
                                   start_time='', 
                                   end_time='', 
                                   is_mute_print=False,
                                   margin_period='5 hours'):
    
    timestamp_start = pd.Timestamp(start_time).tz_localize('UTC').tz_convert('Europe/London')
    timestamp_end = pd.Timestamp(end_time).tz_localize('UTC').tz_convert('Europe/London')
    time_delta_margin_period = pd.Timedelta(margin_period)
    
    timestamp_start_margin = timestamp_start - time_delta_margin_period
    timestamp_end_margin = timestamp_end + time_delta_margin_period
        
    if time_column:
        df = df.set_index(time_column)
    
    if ((df.index.max()+pd.Timedelta('2 min'))  < timestamp_end_margin) or ((df.index.min()-pd.Timedelta('1 min')) > timestamp_start_margin):
        
        return print("Time range is not enough for the specificed period."), print("The required range is", str(timestamp_start_margin), str(timestamp_end_margin))
        
    df_selected_margin_range = df.loc[(df.index >= timestamp_start_margin) &
                                          (df.index < timestamp_end_margin)]
    
    df_selected_margin_range_with_on_off = label_on_off_status_for_all_building_assets(df_selected_margin_range, assets_current_time_margins, is_mute_print=is_mute_print)
    
    # pdb.set_trace()
    
    df_selected_range_with_on_off = df_selected_margin_range_with_on_off.loc[(df_selected_margin_range_with_on_off.index >= timestamp_start) &
                                          (df_selected_margin_range_with_on_off.index < timestamp_end)]
    
    df_selected_range_with_on_off_actions = df_selected_range_with_on_off.loc[df_selected_range_with_on_off.on_off_action != 0]
    
    return df_selected_range_with_on_off_actions, df_selected_range_with_on_off

def calculate_suggested_time_by_weekday(df_enriched_time,
                                        suggested_percentile=50,
                                        operation_action=True):

    def _shift_mod(sr, 
              shift_value = 0, 
              size=24):
        return (sr-shift_value)%size + shift_value

    if operation_action:
        percentile_for_calculation = 1-suggested_percentile/100
        shift_value = -5
    else:
        percentile_for_calculation = suggested_percentile/100
        shift_value = 5

    df_enriched_time_action = df_enriched_time\
        .loc[df_enriched_time['Operation_Action'] == operation_action]
    df_enriched_time_action['time_of_day_in_float'] = _shift_mod(
        df_enriched_time_action['time_of_day_in_float'], shift_value=shift_value)

    # pdb.set_trace()
    
    df_enriched_time_action_suggested = df_enriched_time_action\
        .groupby(['clientid',
                  'Client_Name',
                  'buildingid',
                  'Building_Name',
                  'Asset_Name',
                  'day_of_week'])['time_of_day_in_float']\
        .quantile(percentile_for_calculation)\
        .to_frame()
        
    df_enriched_time_action_suggested['Suggested_Time'] = df_enriched_time_action_suggested['time_of_day_in_float'].apply(time_format_func)

    df_enriched_time_action_suggested['Operation_Action'] = operation_action

    return df_enriched_time_action_suggested.reset_index()

def generate_suggested_time(df_enriched_time,
                            suggested_percentile=50):

    df_with_suggested_time = pd.DataFrame()
    operation_action_list = df_enriched_time['Operation_Action'].unique()
    for operation_action in operation_action_list:
        df_new = calculate_suggested_time_by_weekday(df_enriched_time,
                                                     operation_action=operation_action,
                                                     suggested_percentile=suggested_percentile)
        df_with_suggested_time = df_with_suggested_time.append(df_new)
    
    df_with_suggested_time['Suggested_Time'] = df_with_suggested_time['Suggested_Time'].astype(str)
    df_with_suggested_time['Operation_Action'] = df_with_suggested_time['Operation_Action'].astype(int)
    
    return df_with_suggested_time

def source_to_label_range_shift(start_time, end_time, margin_period, is_initial=False):
    
    time_delta_margin_period = pd.Timedelta(margin_period)
    
    if is_initial:
        label_time_start = (pd.Timestamp(start_time) + time_delta_margin_period).strftime("%Y-%m-%d %H:%M:%S")
    else:
        label_time_start = (pd.Timestamp(start_time) - time_delta_margin_period).strftime("%Y-%m-%d %H:%M:%S")
        
    label_time_end = (pd.Timestamp(end_time) - time_delta_margin_period).strftime("%Y-%m-%d %H:%M:%S")
    
    return label_time_start, label_time_end


