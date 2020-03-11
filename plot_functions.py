
import pandas as pd # import the data as dataframe and manipulate the data
import datetime # to create data-time variables
import matplotlib # to visualize the dataset
import matplotlib.pyplot as plt
import numpy as np
import calendar
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
import seaborn as sns
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from matplotlib.cbook import boxplot_stats

import matplotlib.dates as mdates

def select_the_time_range(df,
                          start_date='2019-07-01',
                          end_date='2020-02-01'):

    timestamp_start = pd.Timestamp(start_date).tz_localize('Europe/London')
    timestamp_end = pd.Timestamp(end_date).tz_localize('Europe/London')

    df = df.loc[(df.index >= timestamp_start) &
                                          (df.index < timestamp_end)]
    return df.reset_index()

def plot_in_barchart(Ben_df_sample_period,
                     concerned_asset = 'Pizza Oven', 
                    concerned_value = 'value',
                    restaurant_name='Braintree',
                    address_to_savefig = False,
                    export_result = False,
                    ot_hms_ls=[0,0,0],
                    ct_hms_ls=[23,59,59]):
    
    if concerned_value == 'cost_in_£':
        y_label_name = '£'
    else:
        y_label_name = 'kWh'
    
    # choose the concerned assets
    Ben_df_sample_period_seleted_facility = Ben_df_sample_period.loc[
        (Ben_df_sample_period.refined_asset_name==concerned_asset)]
        
    opentime =  datetime.time(ot_hms_ls[0], ot_hms_ls[1], ot_hms_ls[2])
    closetime =  datetime.time(ct_hms_ls[0], ct_hms_ls[1], ct_hms_ls[2])
    opentime_str = str(opentime)
    closetime_str = str(closetime)
    Ben_df_sample_period_seleted_facility['opening_period'] = ['yes' if (x.time() >= opentime) & (x.time() <= closetime) else 'no' for x in Ben_df_sample_period_seleted_facility.time]
    Ben_df_open_period_seleted_facility = Ben_df_sample_period_seleted_facility[Ben_df_sample_period_seleted_facility['opening_period']=='yes']
        
    # create a pivot table for plotting figures
    try: 
        Ben_df_open_period_seleted_facility_pivot = Ben_df_open_period_seleted_facility.pivot_table(index='time_of_day', 
                                                                                    columns='day_of_year')[concerned_value]
    except:
        return print('There is no data to plot.')

    plt.figure(figsize=(9,4.5))
    Ben_df_open_period_seleted_facility_pivot.sum().plot(kind='bar', label = 'Daily consumption')
    y_max = Ben_df_open_period_seleted_facility_pivot.sum().max()
    y_min = Ben_df_open_period_seleted_facility_pivot.sum().min()
    plt.title(restaurant_name+', '
              +concerned_asset+'\n daily consumption \n between '
              +opentime_str+' -- '+closetime_str, 
              pad=30)
    plt.ylim([y_min*0.5, y_max*1.25])
    plt.legend(loc='upper right')
    plt.tick_params(axis ='x', rotation =0) 
    plt.xlabel('Day of August')
    plt.ylabel(y_label_name)
    plt.tight_layout() # make room for the xlabel
    if address_to_savefig:
        plt.savefig(address_to_savefig)
    if export_result:
        return Ben_df_open_period_seleted_facility_pivot.sum()
    
def plot_in_barchart_with_ooh(data_source,
                              concerned_asset,
                              concerned_value='value',
                              restaurant_name='Braintree',
                              address_to_savefig=False,
                              show_values=False,
                              figure_width_modifier=2.5,
                              show_proportion=False,
                              export_result=False,
                              figsize=(9, 5.5),
                              ot_hms_ls=[0, 0, 0],
                              ct_hms_ls=[23, 59, 59]):

    if concerned_value == 'cost_in_£':
        y_label_name = '£'
    else:
        y_label_name = 'kWh'

    # choose the concerned assets
    Ben_df_sample_period_seleted_facility = data_source.loc[
        (data_source.refined_asset_name == concerned_asset)]

    opentime = datetime.time(ot_hms_ls[0], ot_hms_ls[1], ot_hms_ls[2])
    closetime = datetime.time(ct_hms_ls[0], ct_hms_ls[1], ct_hms_ls[2])
    opentime_str = str(opentime)
    closetime_str = str(closetime)
    Ben_df_sample_period_seleted_facility['opening_period'] = ['yes' if (x.time() >= opentime) & (
        x.time() <= closetime) else 'no' for x in Ben_df_sample_period_seleted_facility.time]
    Ben_df_open_period_seleted_facility = Ben_df_sample_period_seleted_facility[
        Ben_df_sample_period_seleted_facility['opening_period'] == 'yes']

    # create a pivot table for plotting figures
    try:
        Ben_df_open_period_seleted_facility_pivot = Ben_df_open_period_seleted_facility.pivot_table(index='time_of_day',
                                                                                            columns='date')[concerned_value]
    except:
        return print('The ooh consumption data is empty.')
    
    try:
        Ben_df_total_period_seleted_facility_pivot = Ben_df_sample_period_seleted_facility.pivot_table(index='time_of_day',
                                                                                                columns='date')[concerned_value]
    except:
        return print('There is no data to plot.')
    
    if show_values:
        figsize_0 = Ben_df_total_period_seleted_facility_pivot.shape[1]
        _fig, ax = plt.subplots(figsize=(max(figsize_0/figure_width_modifier, figsize[0]), figsize[1]))
        x_nbins= figsize_0
    else:
        _fig, ax = plt.subplots(figsize=figsize)
        x_nbins= int(Ben_df_total_period_seleted_facility_pivot.shape[1]/figsize[0])
    
    if show_proportion:
        title_tag = ' percentage'
        
        Ben_df_open_period_seleted_facility_pivot.sum().plot(kind='bar', zorder=2, ax=ax,
                                                             label='Consumption ' + opentime_str+' -- '+closetime_str, color='g', alpha=0.7, width=0.8)
        
        Ben_df_total_period_seleted_facility_pivot.sum().plot(ax=ax,
            kind='bar', label='Daily total consumption')
        
        y_max = Ben_df_total_period_seleted_facility_pivot.sum().max()
        y_min = 0  # Ben_df_open_period_seleted_facility_pivot.sum().min()
        if show_values:
            xlocs, _xlabs = plt.xticks()
            for i, (value, prop) in enumerate(zip(Ben_df_total_period_seleted_facility_pivot.sum(), Ben_df_open_period_seleted_facility_pivot.sum()/Ben_df_total_period_seleted_facility_pivot.sum())):
                plt.text(xlocs[i], value + 0.04*(y_max-y_min), 
                         '\n'+str(round(value*prop, 2))+'\n' +
                         '--------\n '+str(round(prop*100, 1))+'%',
                         horizontalalignment='center',
                         label='Consumption value and pct',
                         fontsize=7,
                         fontweight='bold',
                         color='g')
        frame_for_export = {'value': round(Ben_df_open_period_seleted_facility_pivot.sum(), 2),
                 'total': round(Ben_df_total_period_seleted_facility_pivot.sum(), 2),
                 'proportion_pct': round(Ben_df_open_period_seleted_facility_pivot.sum()/Ben_df_total_period_seleted_facility_pivot.sum()*100, 1)}
        df_for_export = pd.DataFrame(frame_for_export)
    else:
        title_tag = ' value'
        Ben_df_open_period_seleted_facility_pivot.sum().plot(kind='bar', ax=ax, label='Consumption '
                                                             + opentime_str+' -- '+closetime_str, color='g', alpha=0.7, width=0.8)
        y_max = Ben_df_open_period_seleted_facility_pivot.sum().max()
        y_min = Ben_df_open_period_seleted_facility_pivot.sum().min()
        if show_values:
            xlocs, _xlabs = plt.xticks()
            for i, v in enumerate(Ben_df_open_period_seleted_facility_pivot.sum()):
                plt.text(xlocs[i], v + 0.02*(y_max-y_min), str(round(v, 2)), 
                         horizontalalignment='center',
                         fontsize=7)
        frame_for_export = {'value': round(Ben_df_open_period_seleted_facility_pivot.sum(), 2)}
        df_for_export = pd.DataFrame(frame_for_export)

    #ax.xaxis.set_major_locator(MultipleLocator(5))
    
    #ax.xaxis.set_minor_locator(MultipleLocator(1))
    
    # for i, xtick_label in enumerate(ax.axes.get_xticks()):
    #     if i % 10 != 0:
    #         xtick_label.set_visible(False)
            
    date_interval_days = Ben_df_total_period_seleted_facility_pivot.shape[1]
    number_of_date_ticks = x_nbins
    date_tick_interval_days = int(date_interval_days / number_of_date_ticks)
    date_ticks = ax.get_xticks()[::date_tick_interval_days]
    date_labels = ax.get_xticklabels()[::date_tick_interval_days]
    ax.set_xticks(date_ticks)
    ax.set_xticklabels(date_labels)
    
    plt.title(restaurant_name+', '
              + concerned_asset+'\n daily consumption' + title_tag + '\n between '
              + opentime_str+' -- '+closetime_str,
              pad=30)
    plt.ylim([y_min*0.5, y_max*1.35])
    plt.legend(loc='upper right')
    plt.tick_params(axis='x', rotation=90)
    #plt.locator_params(axis='x', nbins=x_nbins)
    plt.xlabel('Day of September')
    plt.ylabel(y_label_name)
    plt.tight_layout()  # make room for the xlabel
    if address_to_savefig:
        plt.savefig(address_to_savefig)
    if export_result:
        return df_for_export
    
def plot_in_3d(df_sample_period, assets_3d_plot_good_view,
            concerned_asset='Pizza Oven',
            concerned_value='value',
            restaurant_name='Braintree',
            considered_number_of_days=9,
            index_of_starting_day=0,
            zlim_modifier = 1,
            address_to_savefig=False,
            export_result=False,
            ot_hms_ls=False,
            ct_hms_ls=False,
            view_init_elev=False,
            view_init_azim=False):

    if concerned_value == 'current_value_Amps':
        z_label_name = 'Current value in Amps'
    else:
        z_label_name = concerned_value

    if not ot_hms_ls:
        ot_hms_ls = assets_3d_plot_good_view[concerned_asset]['ot_hms_ls']

    if not ct_hms_ls:
        ct_hms_ls = assets_3d_plot_good_view[concerned_asset]['ct_hms_ls']

    if not view_init_elev:
        view_init_elev = assets_3d_plot_good_view[concerned_asset]['elev']

    if not view_init_azim:
        view_init_azim = assets_3d_plot_good_view[concerned_asset]['azim']

    # choose the concerned assets
    df_sample_period_seleted_facility = df_sample_period.loc[
        (df_sample_period.refined_asset_name == concerned_asset)]

    opentime = datetime.time(ot_hms_ls[0], ot_hms_ls[1], ot_hms_ls[2])
    closetime = datetime.time(ct_hms_ls[0], ct_hms_ls[1], ct_hms_ls[2])
    opentime_str = str(opentime)
    closetime_str = str(closetime)
    df_sample_period_seleted_facility['opening_period'] = ['yes' if (x.time() >= opentime) & (
        x.time() <= closetime) else 'no' for x in df_sample_period_seleted_facility.time]
    df_open_period_seleted_facility = df_sample_period_seleted_facility[
        df_sample_period_seleted_facility['opening_period'] == 'yes']

    # create a pivot table for plotting figures
    try:
        df_open_period_seleted_facility_pivot = df_open_period_seleted_facility.pivot_table(index='time_of_day',
                                                                                            columns='date')[concerned_value]
        if (index_of_starting_day + considered_number_of_days)  > df_open_period_seleted_facility_pivot.shape[1]:
            return print('There is not enough data for the specificed days.')
    except:
        return print('There is no data to plot.')

    fig = plt.figure(figsize=(9, 6))
    ax = fig.gca(projection='3d')

    # considered_number_of_days = len(df_open_period_seleted_facility_pivot.columns)
    xs = np.arange(len(df_open_period_seleted_facility_pivot.index))
    zs = np.arange(considered_number_of_days)
    value_array = np.transpose(np.array(
        df_open_period_seleted_facility_pivot.iloc[:, index_of_starting_day:]))
    verts = []

    for z in zs:
        ys = value_array[z]
        ys[0], ys[-1] = 0, 0
        verts.append(list(zip(xs, ys)))

    palette_1 = sns.color_palette("husl", considered_number_of_days)
    poly = PolyCollection(verts, edgecolors='black', facecolors=palette_1)

    poly.set_alpha(0.7)
    ax.add_collection3d(poly, zs=zs, zdir='y')

    ax.set_title(restaurant_name+', '
                 + concerned_asset+'\n daily consumption 3D plot \n between '
                 + opentime_str+' -- '+closetime_str,
                 pad=40)
    ax.set_xlabel('Time')
    ax.set_xlim3d(np.min(xs)-10, np.max(xs)+10)
    ax.set_ylabel('Day of Year')
    ax.set_ylim3d(0, considered_number_of_days)
    ax.set_zlabel(z_label_name)
    ax.set_zlim3d(0, assets_3d_plot_good_view[concerned_asset]['zlim3d']*zlim_modifier)

    time_interval_mins = np.max(xs) - np.min(xs) + 1
    number_of_time_ticks = 6
    time_tick_interval_mins = int(time_interval_mins / number_of_time_ticks)

    time_range = xs[0::time_tick_interval_mins]
    ax.set_xticks(time_range)
    time_list = [str(
        x) for x in df_open_period_seleted_facility_pivot.index[0::time_tick_interval_mins]]
    ax.set_xticklabels(time_list)

    date_interval_days = np.max(zs) - np.min(zs) + 1
    number_of_date_ticks = 7
    date_tick_interval_days = int(date_interval_days / number_of_date_ticks)
    date_range = zs[0::date_tick_interval_days]
    ax.set_yticks(date_range)
    date_list = [str(
        x) for x in df_open_period_seleted_facility_pivot.columns[index_of_starting_day::date_tick_interval_days]]
    ax.set_yticklabels(date_list)
    ax.view_init(elev=view_init_elev,
                 azim=view_init_azim)
    plt.tight_layout()  # make room for the xlabel
    
    if address_to_savefig:
        plt.savefig(address_to_savefig)

    if export_result:
        return df_open_period_seleted_facility_pivot.sum()

def plot_in_heatmap(df_sample_period,
                    concerned_asset = 'Pizza Oven',
                    concerned_value = 'value',
                    restaurant_name='Braintree',
                    address_to_savefig = False, 
                    max_current = False,
                    ot_hms_ls=[0,0,0],
                    ct_hms_ls=[23,59,59]):
    
    if concerned_value == 'current_value_Amps':
        colorbar_label_name = 'Current value in Amps'
    else:
        colorbar_label_name = concerned_value
        
    # choose the concerned assets
    df_sample_period_seleted_facility = df_sample_period.loc[
        (df_sample_period.refined_asset_name==concerned_asset)]
        
    opentime =  datetime.time(ot_hms_ls[0], ot_hms_ls[1], ot_hms_ls[2])
    closetime =  datetime.time(ct_hms_ls[0], ct_hms_ls[1], ct_hms_ls[2])
    opentime_str = str(opentime)
    closetime_str = str(closetime)
    df_sample_period_seleted_facility['opening_period'] = ['yes' if (x.time() >= opentime) & (x.time() <= closetime) else 'no' for x in df_sample_period_seleted_facility.time]
    df_open_period_seleted_facility = df_sample_period_seleted_facility[df_sample_period_seleted_facility['opening_period']=='yes']
        
    # create a pivot table for plotting figures
    try:
        df_open_period_seleted_facility_pivot = df_open_period_seleted_facility.pivot_table(index='time_of_day',
                                                                                            columns='date')[concerned_value]
    except:
        return print('There is no data to plot.')
    
    if not max_current:
        max_current = df_open_period_seleted_facility_pivot.max().quantile(0.7)*1.1
        
    plt.figure(figsize=(10,6))
    sns.heatmap(df_open_period_seleted_facility_pivot, cmap="Greens", 
                vmin=0,
                vmax=max_current,
                cbar_kws={'label': colorbar_label_name})
    plt.title(restaurant_name+', '
              +concerned_asset+'\n daily consumption heatmap \n between '
              +opentime_str+' -- '+closetime_str, 
              pad=10)
    plt.xlabel('Day of Year')
    plt.ylabel('Time of the day')
    plt.tight_layout() # make room for the xlabel
    
    if address_to_savefig:
        plt.savefig(address_to_savefig)

def format_func(value): # time format function used in the yaxis ticklabel in the boxplot
    
    # find numbers for hour, minute, second 
    value_in_seconds = int(value*3600)
    minute_value, second_value = divmod(value_in_seconds, 60)
    hour_value, minute_value = divmod(minute_value, 60)
    hour_value = hour_value % 24
    #print(hour_value)
    
    return datetime.time(hour_value, minute_value, second_value)

def plot_boxplot(df_sample_period_facility,
                 on_off_action='on_off_action',
                 status_column = 'on_off_perm_status_refined',
                 action='starting',
                 reference_percentile = False,
                 save_plot=False,
                 is_with_duration=True,
                 restaurant_name='Braintree',
                 polished_asset_name='Pizza Oven'):

    # define dependent dataframes for starting points and finishing points
    
    if is_with_duration:
        finishing_action_code = -1
        try:
            df_sample_period_facility[status_column]
        except:
            print("There is no status column in the dataset.")
            return 
    else:
        finishing_action_code = False
        
    if action == 'starting':
        df_sample_period_facility_action_points = df_sample_period_facility.loc[
            (df_sample_period_facility[on_off_action] == 1)]  # 1 means starting action
    else:
        df_sample_period_facility_action_points = df_sample_period_facility.loc[
            (df_sample_period_facility[on_off_action] == finishing_action_code)]  # -1 means finishing action

    _df_sample_period_facility_on_off_for_export = df_sample_period_facility.loc[
        (df_sample_period_facility[on_off_action] != 0)]

    # define the weekday order for the boxplot
    weekday_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    # plot the distribution for starting/finishing action time

    action_time_by_weekdays = [list(group['time_of_day_in_float']) for name,
                               group in df_sample_period_facility_action_points.groupby('day_of_week')]
    action_time_med = [boxplot_stats(group['time_of_day_in_float']).pop(
        0)['med'] for name, group in df_sample_period_facility_action_points.groupby('day_of_week')]
    action_time_fliers = [boxplot_stats(group['time_of_day_in_float']).pop(
        0)['fliers'] for name, group in df_sample_period_facility_action_points.groupby('day_of_week')]
    action_time_whishis = [boxplot_stats(group['time_of_day_in_float']).pop(
        0)['whishi'] for name, group in df_sample_period_facility_action_points.groupby('day_of_week')]
    action_time_whislos = [boxplot_stats(group['time_of_day_in_float']).pop(
        0)['whislo'] for name, group in df_sample_period_facility_action_points.groupby('day_of_week')]
    action_time_whis_max = max(action_time_whishis)
    action_time_whis_min = min(action_time_whislos)
    action_time_whis_range = action_time_whis_max - action_time_whis_min
    
    if action == 'starting':
        
        if reference_percentile:
            reference_time = [np.percentile(a, 100 - reference_percentile) for a in action_time_by_weekdays]
        else:
            reference_time = action_time_whishis
            
        action_time_wasted_time = [[max(y - z, 0) % 24 for z in x]
                                   for x, y in zip(action_time_by_weekdays, reference_time)]
    else:
        
        if reference_percentile:
            reference_time = [np.percentile(a, reference_percentile) for a in action_time_by_weekdays]
        else:
            reference_time = action_time_whislos
            
        action_time_wasted_time = [[max(z - y, 0) % 24 for z in x]
                                   for x, y in zip(action_time_by_weekdays, reference_time)]

    action_time_wasted_timelimit = [
        x - y for x, y in zip(action_time_whishis, action_time_whislos)]
    action_time_wasted_time_refined = [[min(z, y) for z in x] for x, y in zip(
        action_time_wasted_time, action_time_wasted_timelimit)]

    fig = plt.figure(figsize=(8, 7))

    grid = plt.GridSpec(4, 7, hspace=0.5, wspace=0.2)
    ax1 = fig.add_subplot(grid[:3, :])
    ax1.set_ylim([action_time_whis_min - 0.2 * action_time_whis_range,
                  action_time_whis_max + 0.2 * action_time_whis_range])
    ax1 = sns.boxplot(x='day_of_week_abbr_name', y='time_of_day_in_float',
                      order = weekday_order,
                      data=df_sample_period_facility_action_points, width=0.6)
    ax1 = sns.stripplot(x='day_of_week_abbr_name', y='time_of_day_in_float',
                        order = weekday_order,
                        data=df_sample_period_facility_action_points, color="orange", size=6.5)
    ax1.plot([str(calendar.day_abbr[i]) for i in range(7)], [
             11.8 for i in range(7)], linestyle='--', alpha=0.0, color='red')
    labels = [item for item in ax1.get_yticks()]
    ax1.set_yticklabels([format_func(label) for label in labels])
    #ax1.set_xlabel('Week days', labelpad=10)
    ax1.set_xlabel('')
    ax1.set_ylabel(action.title()+' time')
    start_date = df_sample_period_facility_action_points.index.min().strftime("%Y-%m-%d")
    end_date = df_sample_period_facility_action_points.index.max().strftime("%Y-%m-%d")
    ax1.set_title(restaurant_name + ' - ' + polished_asset_name + ' \n' +
                  action.title()+' time distribution \n'+'from '+start_date+' to '+end_date, pad=20)
    #ax1.annotate('Reference starting time: 10:39:00', (str(calendar.day_name[3]), 10.9))
    #ax1.axhline(y=late_starting_time, linestyle='dashed', color='orange', alpha=0.9)
    #ax1.text(x=str(calendar.day_abbr[0]), y=late_starting_time + 0.05 * range_starting_time, s='Reference starting time: '+ str(format_func(late_starting_time)) + ' (Golden line)')
    # fig.autofmt_xdate()
    
    reference_time_lines = [[index, value] for index, value in enumerate(reference_time)]
    
    for day_item in reference_time_lines:
        ax1.annotate('-------', 
                     (str(calendar.day_abbr[day_item[0]]), day_item[1]-0.032*action_time_whis_range),
                     ha = 'center',
                     size=20,
                     color='g', 
                     label = 'legend',
                     alpha=0.9)
    plt.subplots_adjust(top=0.83)

    ax2 = fig.add_subplot(grid[3:, :])

    columns = list(str(calendar.day_abbr[index]) for index in range(7))
    
    if not is_with_duration:
        rows = ['Early time', 'Late time', 'Med time',
                'Outliers', (str(reference_percentile)+'% ref. time' if reference_percentile else 'Ref. time'), 'Accum. (hrs)'] # , 'Total (hrs)', 'Pot. Sav. (%)'
    else:
        rows = ['Early time', 'Late time', 'Med time',
                'Outliers', (str(reference_percentile)+'% ref. time' if reference_percentile else 'Ref. time'), 'Accum. (hrs)', 'Total (hrs)', 'Pot. Sav. (%)'] # 

    data_list = [[0 for x in range(7)] for y in range(len(rows))]

    data_list[1] = [format_func(boxplot_stats(group['time_of_day_in_float']).pop(
        0)['whishi']) for name, group in df_sample_period_facility_action_points.groupby('day_of_week')]
    data_list[0] = [format_func(boxplot_stats(group['time_of_day_in_float']).pop(
        0)['whislo']) for name, group in df_sample_period_facility_action_points.groupby('day_of_week')]
    data_list[5] = [np.around(sum(time), decimals=2)
                    for time in action_time_wasted_time_refined]
    data_list[2] = [format_func(time) for time in action_time_med]
    data_list[3] = [len(fliers) for fliers in action_time_fliers]
    
    data_list[4] = [format_func(reference) for reference in reference_time]
    
    if is_with_duration:
        
        action_time_whishis = [boxplot_stats(group['time_of_day_in_float']).pop(
            0)['whishi'] for name, group in df_sample_period_facility_action_points.groupby('day_of_week')]
        
        df_sample_period_facility_duration = df_sample_period_facility.groupby(['date', 'day_of_week'])[
            status_column].sum().div(60).to_frame(name='duration_mins').reset_index()
        duration_by_weekdays = [list(group['duration_mins']) for name,
                                group in df_sample_period_facility_duration.groupby('day_of_week')]

        data_list[6] = [np.around(sum(time), decimals=2) for time in duration_by_weekdays]
        data_list[7] = [np.around(waste/total*100, decimals=2) for waste, total in zip(data_list[5], data_list[6])]

    ax2.table(cellText=data_list,
              rowLabels=rows,
              colLabels=columns, loc="upper center")
    ax2.axis("off")
    plt.subplots_adjust(left=0.2, bottom=0.2)

    if save_plot:
        address_to_savefig = 'Figures/'
        figure_name = restaurant_name + ' - ' + \
            polished_asset_name + ' - ' + action + ' time boxplot - from '+start_date+' to '+end_date + '.pdf'
        plt.savefig(address_to_savefig+figure_name)






