import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

months_name = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days_name = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for "Chicago", "New York", or "Washington" ?\n').lower()
        if city in ['chicago', 'new york', 'washington']:
            print('Looks like you want to hear about {}!'.format(city))
            break
        else:
            print('please input city name correctly!!!!!')

    # TO DO: get user input for month (all, january, february, ... , june)
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        filter_type = input('Please choose filter type: "month", "day", "both" or "neither".\n').lower()
        if filter_type == 'both':
            month = input('Which month? "January", "February", "March", "April", "May", or "June".\n').lower()
            day = input('Which day? "M", "Tu", "W", "Th", "F", "Sa" or "Su".\n').lower()
        elif filter_type == 'month':
            print('We will make sure to fileter by month!')
            month = input('Which month? "January", "February", "March", "April", "May", or "June".\n').lower()
            day = 'all'
        elif filter_type == 'day':
            print('We will make sure to fileter by day!')
            day = input('Which day? "M", "Tu", "W", "Th", "F", "Sa" or "Su".\n').lower()
            month = 'all'
        elif filter_type == 'neither':
            month = 'all'
            day = 'all'
        else:
            print('please input valid filter_type!!!!!')
            continue

        if month in months_name:
            if day in ['m', 'tu', 'w', 'th', 'f', 'sa', 'su', 'all']:
                break
            else:
                print('please input valid day fileter!!!!!')
        else:
            print('please input valid month fileter!!!!!')

    return filter_type, city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print('Just one moment... Loading the data.')

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek # 0~6
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month']==month]
    if day != 'all':
        days = ['m', 'tu', 'w', 'th', 'f', 'sa', 'su']
        day = days.index(day)
        df = df[df['day_of_week']==day]

    print('-'*40)
    return df


def time_stats(filter_type, df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    max_month = months_name[df['month'].value_counts().index[0]-1].title()
    max_month_count = df['month'].value_counts().iloc[0]
    # TO DO: display the most common day of week
    max_day = days_name[df['day_of_week'].value_counts().index[0]].title()
    max_day_count = df['day_of_week'].value_counts().iloc[0]
    # TO DO: display the most common start hour
    max_hour = df['hour'].value_counts().index[0]
    max_hour_count = df['hour'].value_counts().iloc[0]

    if filter_type == 'both':
        print('Most popular hour:{}, Count:{}'.format(max_hour, max_hour_count))
    elif filter_type == 'month':
        print('Most popular day:{}, Count:{}'.format(max_day, max_day_count))
        print('Most popular hour:{}, Count:{}'.format(max_hour, max_hour_count))
    elif filter_type == 'day':
        print('Most popular month:{}, Count:{}'.format(max_month, max_month_count))
        print('Most popular hour:{}, Count:{}'.format(max_hour, max_hour_count))
    else:
        print('Most popular month:{}, Count:{}'.format(max_month, max_month_count))
        print('Most popular day:{}, Count:{}'.format(max_day, max_day_count))
        print('Most popular hour:{}, Count:{}'.format(max_hour, max_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    max_start = df['Start Station'].value_counts().index[0]
    max_start_count = df['Start Station'].value_counts().values[0]
    # TO DO: display most commonly used end station
    max_end = df['End Station'].value_counts().index[0]
    max_end_count = df['End Station'].value_counts().values[0]

    # TO DO: display most frequent combination of start station and end station trip
    route_df = df.groupby(['Start Station', 'End Station'])
    route_num = route_df.size().sort_values(ascending=False) #对分组后的DataFrame进行计数并排序
    most_route = route_num.iloc[0]
    most_route_num = route_num.value_counts().loc[most_route] #为最大值的路线的数目

    print('Most popular Start Station: {}, Count: {}'.format(max_start, max_start_count))
    print('Most popular End Station: {}, Count: {}'.format(max_end, max_end_count))
    print('the number of the most popular route is {}'.format(most_route_num))
    for x in range(most_route_num):
        print('Most popular route:{}, Count: {}'.format(route_num.index[x], most_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # TO DO: display mean travel time
    total_duration = df['Trip Duration'].sum()
    mean_duration = df['Trip Duration'].mean()
    print('Total Duration: {:.2f}s, Avg Duration: {:.2f}s'.format(total_duration, mean_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(city, df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_counts = df.groupby('User Type').size()
    print('{}:{}, {}:{}'.format(user_counts.index[0], user_counts.iloc[0], \
          user_counts.index[1], user_counts.iloc[1]))

    if city != 'washington':
        # TO DO: Display counts of gender
        gender_counts = df.groupby('Gender').size()
        print('{}:{}, {}:{}'.format(gender_counts.index[0], gender_counts.iloc[0], \
              gender_counts.index[1], gender_counts.iloc[1]))
        
        # TO DO: Display earliest, most recent, and most common year of birth
        birth_df = df.groupby('Birth Year').size()
        birth_index = birth_df.sort_index()
        birth_values = birth_df.sort_values()
        print('earliest year:{}, most recent year:{}'.format(birth_index.index[0], birth_index.index[-1]))
        print('most common year:{}, Count:{}'.format(birth_values.index[-1], birth_values.values[-1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        filter_type, city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(filter_type, df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city, df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
