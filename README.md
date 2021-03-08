# Sparkify Postgres: Data Modeling with Postgres

This project creates a ETL pipeline written in Python to process two different datasets, logs and songs, and load them in a Postgres database with tables designed to optimize queries on song play analysis.

## Datasets

### Song Dataset
The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

`song_data/A/B/C/TRABCEI128F424C983.json`
`song_data/A/A/B/TRAABJL12903CDCF1A.json`

And below is an example of what a single song file, `TRAABJL12903CDCF1A.json`, looks like.

```javascript
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

### Log Dataset
The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.

The log files in the dataset you'll be working with are partitioned by year and month. For example, here are filepaths to two files in this dataset.

`log_data/2018/11/2018-11-12-events.json`
`log_data/2018/11/2018-11-13-events.json`

And below is an example of what the data in a log file, `2018-11-12-events.json`, looks like (just the first 5 rows).

```javascript
{"artist":null,"auth":"Logged In","firstName":"Celeste","gender":"F","itemInSession":0,"lastName":"Williams","length":null,"level":"free","location":"Klamath Falls, OR","method":"GET","page":"Home","registration":1541077528796.0,"sessionId":438,"song":null,"status":200,"ts":1541990217796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/37.0.2062.103 Safari\/537.36\"","userId":"53"}
{"artist":"Pavement","auth":"Logged In","firstName":"Sylvie","gender":"F","itemInSession":0,"lastName":"Cruz","length":99.16036,"level":"free","location":"Washington-Arlington-Alexandria, DC-VA-MD-WV","method":"PUT","page":"NextSong","registration":1540266185796.0,"sessionId":345,"song":"Mercy:The Laundromat","status":200,"ts":1541990258796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.77.4 (KHTML, like Gecko) Version\/7.0.5 Safari\/537.77.4\"","userId":"10"}
{"artist":"Barry Tuckwell\/Academy of St Martin-in-the-Fields\/Sir Neville Marriner","auth":"Logged In","firstName":"Celeste","gender":"F","itemInSession":1,"lastName":"Williams","length":277.15873,"level":"free","location":"Klamath Falls, OR","method":"PUT","page":"NextSong","registration":1541077528796.0,"sessionId":438,"song":"Horn Concerto No. 4 in E flat K495: II. Romance (Andante cantabile)","status":200,"ts":1541990264796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/37.0.2062.103 Safari\/537.36\"","userId":"53"}
{"artist":"Gary Allan","auth":"Logged In","firstName":"Celeste","gender":"F","itemInSession":2,"lastName":"Williams","length":211.22567,"level":"free","location":"Klamath Falls, OR","method":"PUT","page":"NextSong","registration":1541077528796.0,"sessionId":438,"song":"Nothing On But The Radio","status":200,"ts":1541990541796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/37.0.2062.103 Safari\/537.36\"","userId":"53"}
{"artist":null,"auth":"Logged In","firstName":"Jacqueline","gender":"F","itemInSession":0,"lastName":"Lynch","length":null,"level":"paid","location":"Atlanta-Sandy Springs-Roswell, GA","method":"GET","page":"Home","registration":1540223723796.0,"sessionId":389,"song":null,"status":200,"ts":1541990714796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.78.2 (KHTML, like Gecko) Version\/7.0.6 Safari\/537.78.2\"","userId":"29"}
```

## Database

The Postgres database tables were designed to optimize queries on song play analysis. In order to do that, it was created a  star schema including the following tables:

#### Fact Table
 1. **songplays** - records in log data associated with song plays i.e. records with page NextSong
    - songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

#### Dimension Tables
 2. **users** - users in the app
    - *user_id, first_name, last_name, gender, level*
 3. **songs** - songs in music database
    - *song_id, title, artist_id, year, duration*
 4. **artists** - artists in music database
    - *artist_id, name, location, latitude, longitude*
 5. **time** - timestamps of records in songplays broken down into specific units
    - *start_time, hour, day, week, month, year, weekday*



### Prerequisites

The solution was built using Python 3.6.3 and the following package versions are required:
 - **pandas==1.1.5**
 - SQLAlchemy==1.1.13
 - sqlalchemy-schemadisplay==1.3

For the complete package list used to build and run this application, please refer to the file **requirements-env.txt***


### ETL Pipelines
There are two ETLs pipelines in this solution:
 - **etl.py**: It iterates through each json file and create an insert for each entry, after the transformations using pandas dataframe.
 - **etl_alchemy.py**: It iterates through each json file and loads everything into large pandas DataFrames, performs some transformations and uses slqalchemy to perform bulk inserts.

### How to run

```
python create_tables.py
python etl.py
```

Alternatively:

```
python create_tables.py
python etl_alchemy.py
```

In order to generate the database ER diagram, run the following commands:

```
python create_tables.py
python create_erd.png
```


## Analytics

There are some analytics queries in the notebook *analytics.ipynb*.




