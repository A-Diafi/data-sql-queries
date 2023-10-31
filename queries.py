# pylint: disable=C0103, missing-docstring
import sqlite3

def detailed_movies(db):
    '''return the list of movies with their genres and director name'''
    conn = sqlite3.connect('data/movies.sqlite')
    c = conn.cursor()
    query = """
    SELECT movies.title, movies.genres, directors.name
    FROM movies
    JOIN directors ON movies.director_id = directors.id

    """
    c.execute(query)
    rows = c.fetchall()
    list1 = []
    for i in rows:
        list1.append(i)

    return list1


def late_released_movies(db):
    '''return the list of all movies released after their director death'''

    conn = sqlite3.connect('data/movies.sqlite')
    c = conn.cursor()
    query = """
    SELECT movies.title
    FROM movies
    JOIN directors ON movies.director_id = directors.id
    WHERE directors.death_year < movies.start_year

    """
    c.execute(query)
    rows = c.fetchall()
    list1 = []
    for i in range(len(rows)):
        list1.append(rows[i][0])

    return list1

def stats_on(db, genre_name):
    '''return a dict of stats for a given genre'''
    conn = sqlite3.connect('data/movies.sqlite')
    # conn.row_factory = sqlite3.Row
    c = conn.cursor()
    query = """
    SELECT movies.genres AS genre, COUNT(movies.genres) AS number_of_movies, ROUND(AVG(movies.minutes), 2) AS avg_length
    FROM movies
    WHERE movies.genres = ?
    GROUP BY genre
    """
    c.execute(query, (genre_name,))
    rows = c.fetchall()
    DICT1 = {}
    DICT1['genre'] = rows[0][0]
    DICT1['number_of_movies'] = rows[0][1]
    DICT1['avg_length'] = rows[0][2]
    # with the user search, find the result for that genre they have entered
    return DICT1

def top_five_directors_for(db, genre_name):
    '''return the top 5 of the directors with the most movies for a given genre'''
    conn = sqlite3.connect('data/movies.sqlite')
    c = conn.cursor()
    query = """
    SELECT directors.name as name, COUNT(*) as movie_count
    FROM movies
    JOIN directors ON movies.director_id = directors.id
    WHERE movies.genres = ?
    GROUP BY name
    ORDER BY movie_count DESC,name
    LIMIT 5

    """
    c.execute(query, (genre_name,))
    rows = c.fetchall()
    return rows


def movie_duration_buckets(db):
    '''return the movie counts grouped by bucket of 30 min duration'''
    conn = sqlite3.connect('data/movies.sqlite')
    c = conn.cursor()
    query = """
           SELECT
 CASE
    WHEN minutes >= 0 AND minutes < 30 THEN 30
    WHEN minutes >= 30 AND minutes < 60 THEN 60
    WHEN minutes >= 60 AND minutes < 90 THEN 90
    WHEN minutes >= 90 AND minutes < 120 THEN 120
    WHEN minutes >= 120 AND minutes < 150 THEN 150
    WHEN minutes >= 150 AND minutes < 180 THEN 180
    WHEN minutes >= 180 AND minutes < 210 THEN 210
    WHEN minutes >= 210 AND minutes < 240 THEN 240
    WHEN minutes >= 240 AND minutes < 270 THEN 270
    WHEN minutes >= 270 AND minutes < 300 THEN 300
    WHEN minutes >= 300 AND minutes < 330 THEN 330
    WHEN minutes >= 330 AND minutes < 360 THEN 360
    WHEN minutes >= 360 AND minutes < 390 THEN 390
    WHEN minutes >= 390 AND minutes < 420 THEN 420
    WHEN minutes >= 420 AND minutes < 450 THEN 450
    WHEN minutes >= 450 AND minutes < 480 THEN 480
    WHEN minutes >= 480 AND minutes < 510 THEN 510
    WHEN minutes >= 510 AND minutes < 540 THEN 540
    WHEN minutes >= 540 AND minutes < 570 THEN 570
    WHEN minutes >= 570 AND minutes < 600 THEN 600
    WHEN minutes >= 600 AND minutes < 630 THEN 630
    WHEN minutes >= 630 AND minutes < 660 THEN 660
    WHEN minutes >= 660 AND minutes < 690 THEN 690
    WHEN minutes >= 690 AND minutes < 720 THEN 720
    WHEN minutes >= 720 AND minutes < 750 THEN 750
    WHEN minutes >= 750 AND minutes < 780 THEN 780
    WHEN minutes >= 780 AND minutes < 810 THEN 810
    WHEN minutes >= 810 AND minutes < 840 THEN 840
    WHEN minutes >= 840 AND minutes < 870 THEN 870
    WHEN minutes >= 870 AND minutes < 900 THEN 900
    WHEN minutes >= 900 AND minutes < 930 THEN 930
    WHEN minutes >= 930 AND minutes < 960 THEN 960
    WHEN minutes >= 960 AND minutes < 990 THEN 990
    WHEN minutes >= 990 AND minutes < 1020 THEN 1020

 END AS duration_bucket,
 COUNT(*) AS number_of_movies
 FROM movies
 GROUP BY duration_bucket
 ORDER BY duration_bucket
    """
    c.execute(query)
    rows = c.fetchall()
    return rows[1:]

def top_five_youngest_newly_directors(db):
    '''return the top 5 youngest directors when they direct their first movie'''
    conn = sqlite3.connect('data/movies.sqlite')
    c = conn.cursor()
    query = """
    SELECT directors.name as name, (movies.start_year - directors.birth_year) as young
    FROM movies
    JOIN directors ON movies.director_id = directors.id
    WHERE movies.start_year - directors.birth_year
    GROUP BY name
    ORDER BY young ASC
    LIMIT 5
    """
    c.execute(query)
    rows = c.fetchall()
    return rows
