import time
import pandas as pd
import numpy as np
from zipfile import Zipfile

file_name = 'bikeshare-datasets.zip'
with Zipfile(file_name, 'r) as zip:
	zip.extractall()
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():#Done!!
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('\n\nHello! Let\'s explore some US bikeshare data!\n')
    try:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        while True:
            city = input('Would you like to see data for Chicago, New York, or Washington? \n').lower()
            print('')
            if city in CITY_DATA:
                break
            else:
                print('ERROR: Wrong Entry!!, please try again')
                print('\n')
    except:
        print('ERROR!!, please try again')
        print('\n')

    #filtering the file data in furthur details
    while True:
        is_filter = input('Would you like to filter the data by month, day, or not at all? \n').lower()
        print('')
        if is_filter=='not at all' or is_filter=='month' or is_filter=='day':
            if is_filter != 'not at all':
                if is_filter == 'month':
                    # get user input for month (all, january, february, ... , june)
                    while True:
                        month = input('Which month - January, February, March, April, May, or June? \n').lower()
                        print('')
                        if month in MONTHS:
                            day = 'all'
                            while True:
                                again = input('Would you like to filter the data furthur by day, or not at all?\n').lower()
                                print('')
                                if again == 'day':
                                    day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? \n').lower()
                                    print('')
                                    break
                                elif again == 'not at all':
                                    break
                                else:
                                    print('ERROR: Wrong Entry!!, please try again')
                                    print('\n') 
                            break
                        else:
                            print('ERROR: Wrong Entry!!, please try again')
                            print('\n')
                elif is_filter == 'day':
                    # get user input for day of week (all, monday, tuesday, ... sunday)
                    while True:
                        day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? \n').lower()
                        print('\n')
                        month = 'all'
                        if day in DAYS:
                            break
                        else:
                            print('ERROR: Wrong Entry!!, please try again')
                            print('\n')
            else:
                month = 'all'
                day = 'all'
            break
        else:
            print('ERROR: Wrong Entry!!, please try again')
            print('\n')
        
    print('-'*40)
    return city, month, day


def load_data(city, month, day):#Done!!
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #df = pd.read_csv(CITY_DATA[city]) #loading file of specific city
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    #print(df['day_of_week'])

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]
    
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]
    
    return df


def time_stats(df):#Done!!
    """Displays statistics on the most frequent times of travel."""
    print('After filtering the data,\n\nWe\'re Examining a Total of {} rows of data,\n\nLet\'s see what we have on it.....\n\n'.format(
        df.count()[0]))
    print('-'*40)
    print('')

    print('\nCalculating The statistics of Times of Travel...\n \n')
    start_time = time.time()

    print('The Break down of Times of Travels is :\n')
    # display the most common month
    if len(pd.unique(df['month']))!= 1: #testing if there's a choosen month
        print("Users Mostly Travel in {},\t count: {} \n".format(MONTHS[df['month'].mode()[0]-1].title(),
         df[df.month == df['month'].mode()[0]].count()[0]))
    else:
        print("In {},\n".format(MONTHS[df['month'].mode()[0]-1].title()))

    # display the most common day of week
    if len(pd.unique(df['day_of_week']))!=1: #testing if there's a choosen day_of_week
        print("Users Mostly Travel On {},\t count: {} \n".format(df['day_of_week'].mode()[0],
         len(df[df.day_of_week == df['day_of_week'].mode()[0]])))
    else:
        print("On {}s, \n".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print('Users Mostly Travel at {} "in a 24 hour scale". \t count: {} \n'.format(df['hour'].mode()[0],
     len(df[df.hour == df['hour'].mode()[0]])))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)
    print('')


def station_stats(df):#Done!!
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Statistics of Stations and Trip...\n\n')
    start_time = time.time()
    print('The Breakdown of Staions used is :\n')
    # display most commonly used start station
    print('Users Usually Start Their Trips at {} station, \t count: {}\n'.format(df['Start Station'].mode()[0].title(),
     df['Start Station'].value_counts()[df['Start Station'].mode()[0]]))

    # display most commonly used end station
    print('Users Usually End Their Trips at {} station, \t count: {}\n'.format(df['End Station'].mode()[0].title(),
     df['End Station'].value_counts()[df['End Station'].mode()[0]]))

    # display most frequent combination of start station and end station trip
    print("Users Usuallt Take This route {}. \t count: {}\n".format(df.groupby(['Start Station','End Station']).size().idxmax(),
     df.groupby(['Start Station','End Station']).size()[2].sum()))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)
    print('')


def trip_duration_stats(df):#Done!!
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration Statistics...\n')
    start_time = time.time()

    print('The Breakdown of Trip Duration is:\n') 
    # display total travel time
    print('Users spend Max of {} hrs on their trips, \t count: {} \n'.format(time.strftime("%H:%M:%S", time.gmtime(df['Trip Duration'].max())),
     df['Trip Duration'].value_counts()[df['Trip Duration'].max()]))
    print('Users spend Min of {} hrs on their trips, \t count: {} \n'.format(time.strftime("%H:%M:%S", time.gmtime(df['Trip Duration'].min())),
     df['Trip Duration'].value_counts()[df['Trip Duration'].min()]))
    # display mean travel time
    print('Users spend Average of {} hrs on their trips. \t count: {} \n'.format(time.strftime("%H:%M:%S", time.gmtime(df['Trip Duration'].mean())),
     len(df[df.hour== df['Trip Duration'].mean()])))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)
    print('')


def user_stats(df):#Done!!
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Statistics...\n')
    start_time = time.time()

    print('The Beakdown of Users is:\n')
    # Display counts of user types
    print("The Count of each user type is as follows:\n")
    print(df['User Type'].value_counts())
    print('\n')

    # Display counts of gender
    if 'Gender' in df.columns :
        print("The Count of each user gender is as follows:\n")
        print(df['Gender'].value_counts())
        print('\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("The Oldest user was born in {}, \t count: {} \n".format(int(df['Birth Year'].min()),
         df['Birth Year'].value_counts()[df['Birth Year'].min()]))
        print("The Yongest User was born in {}, \t count: {} \n".format(int(df['Birth Year'].max()),
         df['Birth Year'].value_counts()[df['Birth Year'].max()]))
        print("Users of the bikeshare are mostly born in {}.\t count: {} \n".format(int(df['Birth Year'].mode()[0]),
         df['Birth Year'].value_counts()[df['Birth Year'].mode()[0]]))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)
    print('')


def add_stats(df,city,month,day):
    ''' Ask And provide additional statistics about The Data'''
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    while True:
        answer = input('\nWould you like to get furthur Statistical insights about your data, "yes or no" ?\n').lower()
        if answer == 'yes':
            start_time = time.time()
            print('\nYour data is Concerning:\n\nCity: {}\tCount: {} rows of data\n\nMonth: {}\tDay: {}\n\n'.format(
                city, df.count()[0], month, day))
            print('\n\nHere\'s a general Describtive Analysis Insights about The Data:\n\n',
                df.describe(include='object'))
            pd.options.display.float_format = "{:.2f}".format
            print('\n\n', df.describe(include='number'))
            print("\nThis took %s seconds.\n" % (time.time() - start_time))
            break
        elif answer!= 'no':
            print('ERROR: Wrong Entry!!, please try again')
        else:
            break
    
    print('-'*40)
    print('')


def int_insights(df,city,month,day):
    ''' Displaying some insights about The Data'''
    
    while True:
        answer = input('\nWell, How about some interesting observation, "yes or no" ?\n').lower()
        if answer == 'yes':
            start_time = time.time()
            try:
                print('\n\n*** We said that: Users Mostly do their trips at {} "in a 24 hour scale",\
                    \n\tBut the interesting part is most of them start their journy at {} station'.format(df['hour'].mode()[0],
                    df.loc[df['hour']==df['hour'].mode()[0],'Start Station'].iloc[0]))
                
                print("\n\n*** We said that: Users Mostly start their trips at {} station,\
                    \n\tBut The Interesting Part is the data has these Percentage for top 10 starting stations:\n")
                s = df.loc[df['hour']==df['hour'].mode()[0],'Start Station']
                percent100 = s.value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
                print("\t", pd.DataFrame({'per100': percent100}).head(10))

                print("\n\tI imagine That's an interesting fact for the Maketing Team....\n\n")
            except:
                print('')
            print("\nThis took %s seconds.\n" % (time.time() - start_time))
            break
        elif answer!= 'no':
            print('ERROR: Wrong Entry!!, please try again')
        else:
            break

    print('-'*40)
    print('')


def print_data(df):
    """Prompting to ask the user to display data in df."""
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    count = 5
    while True:
        response = input('Would you like to see the raw data ? Enter yes or no.\n').lower()
        if response == 'yes':
            print(df.head())
            response = input('\n\nWould you like to see other set of raw data ? Enter yes or no.\n').lower()
            if response =='yes' and count < df.count()[0]:
                print(df.iloc[count:count+5])
            elif count >= df.count()[0]:
                print('\n\n The Total No. of row data is {} rows.'.format(df.count()[0]))
                break
            else:
                break
        else:
            break
    print('-'*40)
    print('')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
      
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        add_stats(df,city,month,day)
        int_insights(df,city,month,day)
        print_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
