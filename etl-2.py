import os
import glob
import psycopg2
import pandas as pd
import numpy as np
from sql_queries import *


def process_song_file(cur, filepath): 
    """ 
       Reads songs log file row by row, selects needed fields and inserts them into song and artist tables.
       Parameters:
            cur (psycopg2.cursor()): Cursor of the sparkifydb database
            filepath (str): Filepath of the file to be analyzed
    """
    df = pd.read_json(filepath, lines = True)

    song_data = df[["song_id", "title", "artist_id", "year", "duration"]].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    artist_data = df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
       Reads user activity log file row by row, filters by NextSong, selects needed fields, transforms them and inserts
       them into time, user and songplay tables.
       Parameters:
                cur (psycopg2.cursor()): Cursor of the sparkifydb database
                filepath (str): Filepath of the file to be analyzed
    """
    df = pd.read_json(filepath, lines = True)

    df = df[(df['page'] == 'NextSong')]

    t = pd.to_datetime(df['ts'], unit='ms')
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    
    time_data = list((t, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday))
    column_labels = list(('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday'))
    time_df =  pd.DataFrame.from_dict(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    for index, row in df.iterrows():
        
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        songplay_data = (index, row.ts, row.userId, row.level, songid, artistid,       
                         row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
       Walks through all files nested under filepath, and processes all logs found.
       Parameters:
          cur (psycopg2.cursor()): Cursor of the sparkifydb database
          conn (psycopg2.connect()): Connectio to the sparkifycdb database
          filepath (str): Filepath parent of the logs to be analyzed
          func (python function): Function to be used to process each log
       Returns:
          Name of files processed
    """
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
       Function used to extract, transform all data from song and user activity logs and load it into a PostgreSQL DB
       Usage: python etl.py
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()