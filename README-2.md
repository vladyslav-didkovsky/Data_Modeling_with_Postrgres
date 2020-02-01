####Introduction <h4> tag

This this my first Project with Data Engineering - A startup called Sparkify want to analyze the bid data they have been collecting on songs and user activity on their new music streaming app. My mission is analyse and make my client life easier, so we will analyse what the songs users are listening to. The aim is to create a Postgres Database Schema and ETL pipeline to optimize queries for song play analysis.

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
###GENERAL CRITERIA :<h3> tag

#Table Creation <h1> tag

Table creation script runs without errors. The script, create_tables.py, runs in the terminal without errors. The script successfully connects to the Sparkify database, drops any tables if they exist, and creates the tables. Fact and dimensional tables for a star schema are properly defined. CREATE statements in sql_queries.py specify all columns for each of the five tables with the right data types and conditions.

#ETL <h1> tag

ETL script runs without errors. The script, etl.py, runs in the terminal without errors. The script connects to the Sparkify database, extracts and processes the log_data and song_data, and loads data into the five tables. Since this is a subset of the much larger dataset, the solution dataset will only have 1 row match that will populate a songid and an artistid in the fact table. Those are the only 2 values that the query in the sql_queries.py will return. The rest will be none values.ETL script properly processes transformations in Python. INSERT statements are correctly written for each tables and handles existing records where appropriate. songs and artists tables are used to retrieve the correct information for the songplays INSERT.

#Code Quality <h1> tag 

The project shows proper use of documentation. The README file includes a summary of the project, how to run the Python scripts, and an explanation of the files in the repository. Comments are used effectively and each function has a docstring.The project code is clean and modular. Scripts have an intuitive, easy-to-follow structure with code separated into logical functions. Naming for variables and functions follows the PEP8 style guidelines.

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#Project Description: <h1> tag 

Before i start, i had to model data (with Postgres and build and ETL pipeline by using Python) . On the database side, I have to define fact and dimension tables for a Star Schema for a specific focus. On the other hand, ETL pipeline would transfer data from files located in two local directories into these tables in Postgres using Python and SQL. 

#My general steps: <h1> tag 
    
i have to open sql_queries.py . write create, drop, insert, one select statement in that file.. then go to etl.ipynb, create a code as per instruction and apply all those code in etl.py .. and thats it . ( you will write the SQL queries in the sql_queries.py then you will read files and process the data in etl.py then you will submit the sql_queries.py, etl.py and README.md either using gituh or in a zip file)

###Schema for Song Play Analysis <h3> tag

#Context <h1> tag

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app. Your role is to create a database schema and ETL pipeline for this analysis.

This is my presise plan for the first project. 
  
#Data <h1> tag 

Song datasets: all json files are nested in subdirectories under /data/song_data. A sample of this files is:
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
Log datasets: all json files are nested in subdirectories under /data/log_data. A sample of a single row of each files is:
{"artist":"Slipknot","auth":"Logged In","firstName":"Aiden","gender":"M","itemInSession":0,"lastName":"Ramirez","length":192.57424,"level":"paid","location":"New York-Newark-Jersey City, NY-NJ-PA","method":"PUT","page":"NextSong","registration":1540283578796.0,"sessionId":19,"song":"Opium Of The People (Album Version)","status":200,"ts":1541639510796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"20"}

#Database Schema <h1> tag

The schema used for this exercise is the Star Schema: There is one main fact table containing all the measures associated to each event (user song plays), and 4 dimentional tables, each with a primary key that is being referenced from the fact table.

#On why to use a relational database for this case: <h1> tag

*The data types are structured (we know before-hand the sctructure of the jsons we need to analyze, and where and how to extract and transform each field)
*The amount of data we need to analyze is not big enough to require big data related solutions.
*Ability to use SQL that is more than enough for this kind of analysis
*Data needed to answer business questions can be modeled using simple ERD models
*We need to use JOINS for this scenario

#Fact Table <h1> tag

songplays - records in log data associated with song plays i.e. records with page NextSong

1.songplay_id (INT) PRIMARY KEY: ID of each user song play
1.start_time (DATE) NOT NULL: Timestamp of beggining of user activity
1.user_id (INT) NOT NULL: ID of user
1.level (TEXT): User level {free | paid}
1.song_id (TEXT) NOT NULL: ID of Song played
1.artist_id (TEXT) NOT NULL: ID of Artist of the song played
1.session_id (INT): ID of the user Session
1.location (TEXT): User location
1.user_agent (TEXT): Agent used by user to access Sparkify platform

#Dimension Tables <h1> tag

users - users in the app

*user_id (INT) PRIMARY KEY: ID of user
*first_name (TEXT) NOT NULL: Name of user
*last_name (TEXT) NOT NULL: Last Name of user
*gender (TEXT): Gender of user {M | F}
*level (TEXT): User level {free | paid}
*songs - songs in music database

*song_id (TEXT) PRIMARY KEY: ID of Song
*title (TEXT) NOT NULL: Title of Song
*artist_id (TEXT) NOT NULL: ID of song Artist
*year (INT): Year of song release
*duration (FLOAT) NOT NULL: Song duration in milliseconds
*artists - artists in music database

*artist_id (TEXT) PRIMARY KEY: ID of Artist
*name (TEXT) NOT NULL: Name of Artist
*location (TEXT): Name of Artist city
*lattitude (FLOAT): Lattitude location of artist
*longitude (FLOAT): Longitude location of artist
*time - timestamps of records in songplays broken down into specific units

*start_time (DATE) PRIMARY KEY: Timestamp of row
*hour (INT): Hour associated to start_time
*day (INT): Day associated to start_time
*week (INT): Week of year associated to start_time
*month (INT): Month associated to start_time
*year (INT): Year associated to start_time
*weekday (TEXT): Name of week day associated to start_time

###Project structure <h3> tag

#Files used on the project:<h1> tag 

*data folder nested at the home of the project, where all needed jsons reside.
*sql_queries.py contains all your sql queries, and is imported into the files bellow.
*create_tables.py drops and creates tables. You run this file to reset your tables before each time you run your ETL scripts.
*test.ipynb displays the first few rows of each table to let you check your database.
*etl.ipynb reads and processes a single file from song_data and log_data and loads the data into your tables.
*etl.py reads and processes files from song_data and log_data and loads them into your tables.
*README.md current file, provides discussion on my project.

#Cheats. Just follow these steps:

1º Wrote DROP, CREATE and INSERT query statements in sql_queries.py

2º Run in console

python create_tables.py
3º Used test.ipynb Jupyter Notebook to interactively verify that all tables were created correctly.

4º Followed the instructions and completed etl.ipynb Notebook to create the blueprint of the pipeline to process and insert all data into the tables.

5º Once verified that base steps were correct by checking with test.ipynb, filled in etl.py program.

6º Run etl in console, and verify results:

*python etl.py
*ETL pipeline

#Prerequisites:<h1> tag

Database and tables created
On the etl.py we start our program by connecting to the sparkify database, and begin by processing all songs related data.

We walk through the tree files under /data/song_data, and for each json file encountered we send the file to a function called process_song_file.

Here we load the file as a dataframe using a pandas function called read_json().

#For each row in the dataframe we select the fields we are interested in:<h1> tag

song_data = [song_id, title, artist_id, year, duration]
artist_data = [artist_id, artist_name, artist_location, artist_longitude, artist_latitude]
    
And finally we insert this data into their respective databases.

Once all files from song_data are read and processed, we move on processing log_data.

We repeat step 2, but this time we send our files to function process_log_file.

We load our data as a dataframe same way as with songs data.

We select rows where page = 'NextSong' only

We convert ts column where we have our start_time as timestamp in millisencs to datetime format. We obtain the parameters we need from this date (day, hour, week, etc), and insert everythin into our time dimentional table.

Next we load user data into our user table

Finally we lookup song and artist id from their tables by song name, artist name and song duration that we have on our song play data. The query used is the following:

song_select = ("""
    SELECT song_id, artists.artist_id
    FROM songs JOIN artists ON songs.artist_id = artists.artist_id
    WHERE songs.title = %s
    AND artists.name = %s
    AND songs.duration = %s
""")
The last step is inserting everything we need into our songplay fact table.

#######WOW, look at that u have done it:D <h7> tag 
