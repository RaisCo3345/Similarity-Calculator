
import csv
import logging

"""  
I used log Exception to helps me create a record of what happens when the program runs. 
and its very important because it lets us track any issues and see what the program did, 
which is very helpful for debugging, The logger tells us when the exception occurred, 
and the exception type, Since we want our logger to write to a file, we need to update 
the configuration to point to the file (exception_data.log). if the file don't exist 
Python will automatically create the file us. Using INFO to record informational messages, 
warnings and errors. "format" control how each log entry will look when written to the file.
"datefmt" controls how the date and time will be formatted in our record.
"""
logging.basicConfig(
    filename='exception_data.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%y-%m-%d %H:%M:%S',
)

def data_file(my_data):
    """
    This function returns My data which is the music data grouped by artist. If when uploading the file
    something goes wrong like the file does not exist, has errors or corrupt data it simply returns an
    empty dictionary instead of crashing. All issues are written to a log file for review.

    """
    artist_file = {}
    try:
        with open(my_data, 'r', encoding='utf-8') as my_file:
            file = csv.reader(my_file)
            header = next(file)

            for row in file:
                artists = row[header.index('artists')][2:-2].split("', '")
                track_name = row[header.index('name')]
                corresponding_features = {
                    'acousticness': float(row[header.index('acousticness')]),
                    'danceability': float(row[header.index('danceability')]),
                    'energy': float(row[header.index('energy')]),
                    'id': row[header.index('id')],
                    'liveness': float(row[header.index('liveness')]),
                    'loudness': float(row[header.index('loudness')]),
                    'name': track_name,
                    'popularity': int(row[header.index('popularity')]),
                    'speechiness': float(row[header.index('speechiness')]),
                    'tempo': float(row[header.index('tempo')]),
                    'valence': float(row[header.index('valence')])
                }

                for artist in artists:
                    if artist not in artist_file:
                        artist_file[artist] = {}
                    artist_file[artist][track_name] = corresponding_features

        logging.info(f'Loaded {len(artist_file)} artists from {my_data}')
        return artist_file

    except FileNotFoundError as e:
        logging.error(f'File not found: {my_data}: {e}')
        return {}
    except Exception as e:
        logging.error(f'Error loading {my_data}: {e}')
        return {}
