import os
import glob
import pandas as pd
from sql_queries import *
from sqlalchemy import create_engine


def process_song_file(engine, df):
    """
    This procedure processes a given dataframe and uses the pandas to_sql function to perform bulk inserts.
    It extracts the song information in the dataframe in order to store it into the songs table.
    Then it extracts the artist information in the dataframe in order to store it into the artists table.

    INPUTS: 
    * cur the cursor variable
    * filepath the file path to the song file
    """
    # load songs
    songs_df = df[['song_id', 'title', 'artist_id', 'year', 'duration']]
    songs_df.to_sql('songs', engine, if_exists='replace', chunksize=500, method='multi', index=False)
    print(" -> songs data loaded")
    
    # load artists
    artists_df = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    artists_df = artists_df.rename(columns={"artist_name" : "name", 
                                            "artist_location" : "location", 
                                            "artist_latitude" : 
                                            "latitude", 
                                            "artist_longitude":"longitude"})

    artists_df.to_sql('artists', engine, if_exists='replace', chunksize=500, method='multi', index=False)
    print(" -> artists data loaded")


def process_log_file(engine, df):
    """
    This procedure processes a given dataframe and uses the pandas to_sql function to perform bulk inserts.
    It extracts the log information in order to store it into the tables: time, users, and songplays.
    
    INPUTS: 
    * cur the cursor variable
    * filepath the file path to the song file
    """
    
    # filter by NextSong action
    df = df[df["page"]=="NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"], unit='ms')
    
    # load time data records
    time_data = [df.ts.values, t.dt.hour.values, t.dt.day.values, t.dt.isocalendar().week.values, t.dt.month.values, t.dt.year.values, t.dt.weekday.values]
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(pd.Series(time_data,index=column_labels).to_dict())
    time_df.to_sql('time', engine, if_exists='replace', chunksize=500, method='multi', index=False)
    print(" -> time data loaded")

    # load users
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    user_df = user_df.rename(columns={"userId" : "user_id", 
                                      "firstName" : "first_name", 
                                      "lastName" : "last_name"})

    user_df.to_sql('users', engine, if_exists='replace', chunksize=500, method='multi', index=False)
    print(" -> users data loaded")

    # insert songplay records
    print(" -> inserting songplay records...")
    with engine.begin() as con:
        for index, row in df.iterrows():

            results = con.execute(song_select, (row.song, row.artist, row.length)).fetchone()
        
            if results:
                songid, artistid = results
            else:
                songid, artistid = None, None

            # insert songplay record
            songplay_data = [row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
            con.execute(songplay_table_insert, songplay_data)
    print(" -> songplay records loaded")


def process_data(engine, filepath, func):
    """
    This procedure crawls into the given directory, reads the json files and creates a single dataframe with all the data.
    Then, it calls the function to handle the dataframes.
    
    INPUTS: 
    * engine the sqlalchemy engine variable
    * filepath the file path to the datasets (songs or logs)
    * func the specific function to process the dataframes
    """       
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    dfs = [] # an empty list to store the data frames

    for datafile in all_files:
        data = pd.read_json(datafile, lines=True)
        dfs.append(data) 
    
    temp = pd.concat(dfs, ignore_index=True)
    func(engine, temp)


def main():
    """
    This is the main code.
    It creates the sqlalchemy database engine and call the functions that will process each type of files.
    """      
    engine = create_engine('postgresql+psycopg2://student:student@localhost:5432/sparkifydb')

    process_data(engine, filepath='data/song_data', func=process_song_file)
    process_data(engine, filepath='data/log_data',  func=process_log_file)

if __name__ == "__main__":
    main()