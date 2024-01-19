"""Import python modules required for all functions below."""

import datetime
import pandas as pd
import calendar
from math import floor
# Note: imports below commented out because they were not used or required
# import time
# import numpy as np


CITY_DATA = {'Chicago': 'chicago.csv',
             'New York city': 'new_york_city.csv',
             'Washington DC': 'washington.csv'}
CITY__OPT_INPUTS = ['c', 'n', 'w']
FILTER_OPT_INPUTS = ['m', 'd', 'n', 'b']
PAGER_VIEW_INPUTS = ['b', 'q', '']
PAGER_PROMPT_INPUTS = ['', 'y', 's']
DF_OUTPUT_PAGE_SIZE = 5
APP_INIT_BANNER = ''' _   _ ____    ____  _ _          ____  _                                      _           _     _             ____ _____ ____ 
| | | / ___|  | __ )(_) | _____  / ___|| |__   __ _ _ __ ___   _ __  _ __ ___ (_) ___  ___| |_  | |__  _   _  | __ )_   _/ ___|
| | | \___ \  |  _ \| | |/ / _ \ \___ \| '_ \ / _` | '__/ _ \ | '_ \| '__/ _ \| |/ _ \/ __| __| | '_ \| | | | |  _ \ | || |    
| |_| |___) | | |_) | |   <  __/  ___) | | | | (_| | | |  __/ | |_) | | | (_) | |  __/ (__| |_  | |_) | |_| | | |_) || || |___ 
 \___/|____/  |____/|_|_|\_\___| |____/|_| |_|\__,_|_|  \___| | .__/|_|  \___// |\___|\___|\__| |_.__/ \__, | |____/ |_| \____|
                                                              |_|           |__/                       |___/                   '''


def weekday_num2str(day):
    """
    Convert weekday number (0:6) to its full name.

    Arguments:
        day -- number (0:6)

    Returns:
        full name (str) e.g. "Sunday"
    """
    return calendar.day_name[calendar.day_abbr[0:7].index(day)]


def month_abbr2name(month_abbr):
    """
    Convert 3 char abbr of a month to its full name.

    Arguments:
        month_abbr -- e.g. "Jan" (str)

    Returns:
        full name (str) e.g. "January"
    """
    return
    calendar.month_name[calendar.month_abbr[1:13].index(month_abbr.title())+1]


def month_num2name(month_number):
    """
    Convert month's number to its full name.

    Arguments:
        month_number -- (1:12) int

    Returns:
        full name of month, e.g. 'January'
    """
    return calendar.month_name[month_number-1]


def dictionary_prettyprint(d):
    """
    Print nicely aligned columns of a dictionary's key & value pairs.

    Arguments:
        d -- the dictionary to pretty print
    """
    for k, v in d.items():
        print('{thekey}{pad}{theval}'.
              format(thekey=k,
                     pad=' '.rjust(48-len(k)),
                     theval=v))


def df_column_items_dist_print(df, col_str):
    r"""
    Print distribution counts of the different values in a given dataframe
    column with column check.

    Note if the column doesn't exist in the dataframe, this will alert the
    user and not throw an error.

    Arguments:
        df -- the dataframe\n
        col_str -- the column string of the dataframe to query
    """
    if col_str in df.columns:
        genders = df[col_str].value_counts()
        print(genders.to_string()+'\n')
    else:
        print('\nSorry, no data available about ' +
              '{this_col} for the selected city'.
              format(this_col=col_str))


def print_bikeshare_df_page(df, index):
    """
    Print rows of df param dataframe, using index param and
    DF_OUTPUT_PAGE_SIZE to print specific rows via df.iloc().

    This calls get_pager_input() to set newindex which controls scrolling
    forward or back, or exit.
    If newindex is valid, recursively calls itself using newindex.
    Also check the current index to prevant scrolling outside of dataframe
    start or end this method doesn't return anything.

    Arguments:
        df -- the dataframe
        index -- int to point to specific range of rows in the dataframe
    """
    if index < 0:
        index = 0  # Prevent backscrolling past first line of the df.
    if (index < (len(df)-DF_OUTPUT_PAGE_SIZE)):
        print(df.iloc[index:index+DF_OUTPUT_PAGE_SIZE])
        newindex = get_pager_input(index)
        if newindex is not None:
            print_bikeshare_df_page(df, newindex)
    else:
        print('\nEnd of dataframe.\n')


def get_pager_input(index):
    """
    Get user input while user is viewing pages of the filtered dataframe.

    If invalid input received, this method just will keep calling itself
    recursively until getting a valid input.

    Arguments:
        index -- the current index value pointing to the first row of the
        dataframe page being viewed

    Returns:
        new index value: None aborts viewing, or index +/- by
        DF_OUTPUT_PAGE_SIZE for view of next or prev df page
    """
    more_prompt = input('\nPress [Enter] key to view next page,' +
                        ' [b] to view previous page, ' +
                        'or enter [q] to exit ...\n')
    if more_prompt[0:1] in PAGER_VIEW_INPUTS:
        match more_prompt[0:1]:
            case '':
                newindex = index+DF_OUTPUT_PAGE_SIZE
            case 'b':
                newindex = index-DF_OUTPUT_PAGE_SIZE
            case 'q':
                newindex = None
                print('\n[Exiting query results view]')
    else:
        print('Invalid input, please try again')
        newindex = get_pager_input(index)
    return newindex


def input_city():
    """
    Get city option from user to match key in CITY_DATA, so that proper
    CSV file is read.

    If invalid input received, this method just will keep calling itself
    recursively until getting a valid input.

    Returns:
       'Chicago' | 'Washington DC' | 'New York city' (str)
    """
    city_prompt = input('\nWhich city Chicago [C], New York [N], or ' +
                        'Washington [W] would you like to select? ')
    city_char = city_prompt[0:1].lower()
    if city_char in CITY__OPT_INPUTS:
        match city_char:
            case 'c':
                city = 'Chicago'
            case 'w':
                city = 'Washington DC'
            case 'n':
                city = 'New York city'
        result = city
    else:
        print('Invalid input, please try again')
        result = input_city()
    return result


def input_month():
    """
    Get month filter option from user.

    Options match 3 char abbr's for months: ['Jan'], ['Feb'], .. ['Dec']
    (calendar.month_abbr[1:13]).
    If invalid input received, this method just will keep calling itself
    recursively until getting a valid input.

    Returns:
        specific 'Jan'|'Feb'|..|'Dec' (3 char str)
    """
    month_prompt = input('\nPlease specify the month ' +
                         '(enter the first 3 letters: ' +
                         '[Jan], [Feb], .. [Dec]): ')
    month_entered = month_prompt[0:3].title()
    if month_entered in calendar.month_abbr[1:13]:
        result = month_entered
    else:
        print('Invalid input, please try again')
        result = input_month()
    return result


def input_filter_opt():
    """
    Get data filter option from user.

    Options are to filter by month [M], day [D], both month and day [B], or
    not at all/all rows [N].
    If invalid input received, this method just will keep calling itself
    recursively until getting a valid input.

    Returns:
        'm'|'d'|'b'|'n' (1 char string)
    """
    filter_prompt = input('\nWould you like to filter city data ' +
                          'by month [M], day [D], both month & day [B], ' +
                          'or not at all [N]? ')
    filter_entered = filter_prompt[0:1].lower()
    if filter_entered in FILTER_OPT_INPUTS:
        result = filter_entered
    else:
        print('Invalid input, please try again')
        result = input_filter_opt()
    return result


def input_day_of_week():
    """
    Get specific weekday from the user.

    If invalid input received, this method just will keep calling itself
    recursively until getting a valid input.

    Returns:
       'Sun'|'Mon'| ... |'Sat' (string)
    """
    dow_prompt = input('\nPlease specify the day of week ' +
                       '(first 3 letters: [Mon], [Tue], .. [Sun]): ')
    dow_entered = dow_prompt[0:3].title()
    if dow_entered in calendar.day_abbr[0:7]:
        result = dow_entered
    else:
        print('Invalid input, please try again')
        result = input_day_of_week()
    return result


def confirm_df_view():
    """
    Ask user if they want to view the dataframe resulting from the query.

    If invalid input received, this method just will keep calling itself
    recursively until getting a valid input.

    Returns:
         True (yes - view it) or False (skip viewing)
    """
    df_view_start_prompt = input('\nWould you now like to view the dataframe' +
                                 ' for this query? Press [Enter] or ' +
                                 'enter [y] to proceed, or [s] to skip ')
    if df_view_start_prompt[0:1].lower() in PAGER_PROMPT_INPUTS:
        match df_view_start_prompt[0:1].lower():
            case '' | 'y': return True
            case 's': return False
    else:
        print('Invalid input, please try again')
        confirm_df_view()


def get_filters():
    """
    Ask user to specify a city, month, and day to analyze.

    Returns:
        city
            name of the city to analyze (str)
        month
            name of the month to filter by,
            or "all" to apply no month filter (str)
        day
            name of the day of week to filter by,
            or "all" to apply no day filter (str)
    """
    day = 'all'
    month = 'all'
    city = input_city()

    match input_filter_opt():
        case 'd':
            day = input_day_of_week()
            weekday_name = weekday_num2str(day)
            print('\n------- Rental Summary Statistics & Dataset Rows for ' +
                  '{cname} on {daystr}s -------\n'.
                  format(cname=city, daystr=weekday_name))
        case 'm':
            month = input_month()
            month_name = month_abbr2name(month)
            print('\n------- Rental Summary Statistics & Dataset Rows for ' +
                  '{cname} in {monthstr} -------\n'.
                  format(cname=city, monthstr=month_name))
        case 'b':
            day = input_day_of_week()
            weekday_name = weekday_num2str(day)
            month = input_month()
            month_name = month_abbr2name(month)
            print('\n------- Rental Summary Statistics & Dataset Rows for ' +
                  '{cname} in {monthstr} on {daystr}s -------\n'.
                  format(cname=city, monthstr=month_name, daystr=weekday_name))
        case 'n': print('\n------- All rentals for city {cname} -------\n'.
                        format(cname=city))
    return city, month, day


def load_data(city, month, day):
    """
    Load data for the specified city and filters by month and/or
    day if applicable.

    Arguments:
        city
            name of the city to analyze, i.e. which CSV file to read (str)
        month
            name of the month to filter by, or "all" to apply no month
            filter (str)
        day
            name of the day of week to filter by, or "all" to apply no day
            filter (str)

    Returns:
        df
            dataframe containing city data filtered by month and day
    """
    city_csv = CITY_DATA[city]
    df = pd.read_csv(city_csv, delimiter=',', index_col=0)
    # Call update_df_columns below to make needed changes on the dataframe.
    df = update_df_columns(month, day, df)
    return df


def update_df_columns(month, day, df):
    """
    Modify & add new df columns for filters and summary stat calc
    methods below.

    Checks day and month params to determine whether those filters should
    be applied

    Arguments:
        month
            month (3 char str, e.g. 'Jan')
        day
            day (3 char str, e.g. 'Mon')
        df
            the dataframe to update

    Returns:
       modified dataframe (df)
    """
    # Convert Start and End Time columns to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'],
                                      format='%Y-%m-%d %H:%M:%S')
    df['End Time'] = pd.to_datetime(df['End Time'], format='%Y-%m-%d %H:%M:%S')

    # Now we can create new derived columns for filter options below.
    df['Month Number'] = (df['Start Time']).dt.month
    df['Weekday Name'] = (df['Start Time']).dt.day_name()

    if month != 'all':
        # Use the index of the months list to get the corresponding int.
        monthnum = calendar.month_abbr[1:13].index(month.title())+1
        # filter by month within the dataframe
        df = df[df['Month Number'] == monthnum]

    if day != 'all':
        # Filter by weekday within the dataframe.
        weekday_str = weekday_num2str(day)
        df = df[df['Weekday Name'] == weekday_str]
    return df


def time_stats(df, month, day):
    """
    Display statistics on the most frequent times of travel.

    Uses local dictionary var time_stats_dict to collect the stats,
    then pretty-prints that.

    Arguments:
        df
            the source dataframe
        month
            month filter
        day
            day filter
    """
    print('*** Most Frequent Times of Travel ***\n')

    time_stats_dict = {}

    # Don't bother with Busiest Month if the user has
    # filtered the df to a specific month already.
    if month == 'all':
        top_month_number = df['Month Number'].value_counts().idxmax()
        top_month = month_num2name(top_month_number)
        time_stats_dict['Busiest month'] = top_month

    # Don't bother with Busiest Weekday if the user has
    # filtered the df to a specific day already.
    if day == 'all':
        top_weekday = df['Weekday Name'].value_counts().idxmax()
        time_stats_dict['Busiest day of the week'] = top_weekday

    # Display the most common start hour.
    df['Start Hour'] = df['Start Time'].dt.hour
    top_start_hr = df['Start Hour'].value_counts().idxmax()
    # Convert this to something more human readable.
    if top_start_hr < 12:
        am_pm_str = ' am'
    else:
        am_pm_str = ' pm'
        if top_start_hr > 12:
            top_start_hr = top_start_hr-12
    time_stats_dict['Busiest Start Hour'] = str(top_start_hr)+am_pm_str

    dictionary_prettyprint(time_stats_dict)


def station_stats(df):
    """
    Display statistics on the most popular stations and trip.

    Uses local dictionary var station_stats_dict to collect the stats,
    then pretty-prints that.

    Arguments:
        df: the source dataframe
    """
    print('\n*** Station Statistics ***\n')

    station_stats_dict = {}

    # Display most commonly used start station.
    top_start_station = df['Start Station'].value_counts().idxmax()
    station_stats_dict['Most frequented Start Station'] = top_start_station

    # Display most commonly used end station.
    top_end_station = df['End Station'].value_counts().idxmax()
    station_stats_dict['Most frequented End Station'] = top_end_station

    # Display most frequent combination of start station and end station trip.
    df['Start+End Stations'] = df.apply(lambda x: '%s to %s' %
                                        (x['Start Station'],
                                         x['End Station']), axis=1)
    top_journey = df['Start+End Stations'].value_counts().idxmax()
    station_stats_dict['Most common journey (Start+End)'] = top_journey

    dictionary_prettyprint(station_stats_dict)


def trip_duration_stats(df):
    """
    Display statistics on the total and average trip duration.

    Uses local dictionary var trip_duration_dict to collect the stats,
    then pretty-prints that.

    Arguments:
        df -- the dataframe
    """
    print('\n*** Trip Duration Statistics ***\n')
    trip_duration_dict = {}
    # Using datetime.timedelta for more user-friendly output
    # rather than just XXXXXXX seconds.
    total_duration_trips = str(datetime.timedelta(
        seconds=df['Trip Duration'].sum().round().astype(float)))
    trip_duration_dict['Total duration of trips'] = total_duration_trips
    mean_duration_trips = str(datetime.timedelta(
        seconds=df['Trip Duration'].mean().round().astype(float)))
    trip_duration_dict['Mean duration of trips'] = mean_duration_trips

    dictionary_prettyprint(trip_duration_dict)


def user_stats(df, day):
    """
    Display statistics on bikeshare users (riders).

    Uses both df_column_items_dist_print() and dictionary_prettyprint() methods
    depending on the kind of data being summarized from the dataframe column.

    Arguments:
        df
            the dataframe
        day
            day filter ('all' or specific day)
    """
    print('\n*** Rider Statistics ***\n')
    user_stats_dict = {}
    # Display counts of user types
    df_column_items_dist_print(df, 'User Type')
    # Display counts of gender
    df_column_items_dist_print(df, 'Gender')

    if day == 'all':
        print('\n* Total ridership over all weekdays (highest to lowest) *')
        df_column_items_dist_print(df, 'Weekday Name')
    else:
        print('\n* Total ridership on selected day *')
        df_column_items_dist_print(df, 'Weekday Name')

    if 'Birth Year' in df.columns:
        least_recent_birthyear = df['Birth Year'].min()
        user_stats_dict['Birth year of oldest rider'] = (
                        floor(least_recent_birthyear))
        most_recent_birthyear = df['Birth Year'].max()
        user_stats_dict['Birth year of youngest rider'] = (
                        floor(most_recent_birthyear))
        most_common_birthyear = df['Birth Year'].value_counts().idxmax()
        user_stats_dict['Most common birth year'] = (
                        floor(most_common_birthyear))
        dictionary_prettyprint(user_stats_dict)
    else:
        print('\nSorry, no rider age data available for this city')


def print_summary_stats(df, month, day):
    """
    Print all Summary Statistics.

    Top level method calling all other methods for printing Summary Statistics.

    Arguments:
        df
            the dataframe
        month
            month filter (str)
        day
            day filter (str)
    """
    print('******* Summary Statistics *******\n')
    time_stats(df, month, day)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df, day)
    print('(end of Summary Statistics)\n')


def main():
    """
    Run main block of code for this Bikeshare python file.

    This greets the user and invokes main event loop (Apple HQ address street
    named "1 Infinite Loop" for good reason!).
    The only way the event loop ends normally is if the user elects to quit,
    which breaks out of this main event loop.
    """
    print('\033c'+APP_INIT_BANNER)
    while True:
        # Get filters from user for data query.
        print('\nPlease select which parts of the bikeshare data & ' +
              'associated statistics you want to view below.')
        city, month, day = get_filters()
        # Load city data per user's query city/month/day filter options.
        df = load_data(city, month, day)
        # Make sure we actually have some data!
        # CSVs don't have any records for July-Dec ;-).
        if len(df) > 0:
            print_summary_stats(df, month, day)
            if confirm_df_view():
                print('\n** Dataset rows **\n')
                print_bikeshare_df_page(df, 0)
            else:
                print('[OK, skipping dataframe view ...]')
        else:
            print('\nSorry, no matching data found with the selected ' +
                  'filters! Please try changing your filter options.')

        restart_prompt = input('\nWould you like to make a new query? ' +
                               'Enter [y] to start again, otherwise ' +
                               'enter anything else to quit completely.\n')
        match restart_prompt[0:1].lower():
            case 'y':
                print('\nRestarting ...\n \033c')
            case _:
                print('Bye! See you again soon, thanks :-) !')
                break


if __name__ == "__main__":
    """
    main Execute when the module is not initialized from an import statement.\n
    """
    main()
