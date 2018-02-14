#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is a internal reporting tool program to be run from the command line.

It uses information from a mock newspaper database to display what kind of
articles a newspaper site's readers like by answering the following questions.

1. What are the most popular three articles of all time?

2. Who are the most popular article authors of all time?

3. On which days did more than 1% of requests lead to errors?
"""


import psycopg2


DBNAME = "news"


def top3articles():
    """Generate & display the most popular three articles of all time.

    NOTE: Relies on the log_path_num_nolimit sql view,
    please see README.md for details.
    """
    top3_query = '''
        SELECT articles.title, num FROM articles, log_path_num_nolimit
        WHERE log_path_num_nolimit.path =
        CONCAT('/article/',articles.slug) LIMIT 3
    '''
    conn = psycopg2.connect(database=DBNAME)
    cursor = conn.cursor()
    cursor.execute(top3_query)
    results = cursor.fetchall()
    print("")
    print("The most popular three articles of all time are:")
    print("")
    for i in range(len(results)):
        path = results[i][0]
        views = results[i][1]
        print("%s -- %d" % (path, views) + " views")
    conn.close()

    return results


def topAuthors():
    """Generate & display the most popular article authors of all time."""
    top_authors_query = '''
        SELECT authors.name, count(log.path) AS views
        FROM log JOIN articles ON log.path = CONCAT('/article/', articles.slug)
        JOIN authors ON authors.id = articles.author
        WHERE status = '200 OK'
        GROUP BY authors.name
        ORDER BY views desc
    '''
    conn = psycopg2.connect(database=DBNAME)
    cursor = conn.cursor()
    cursor.execute(top_authors_query)
    results = cursor.fetchall()
    print("")
    print("The most popular article authors of all time are:")
    print("")
    for i in range(len(results)):
        authors = results[i][0]
        views = results[i][1]
        print("%s -- %d" % (authors, views) + " views")
    conn.close()

    return results


def PercentageErrorDates():
    """Display the days where more than 1% of requests lead to errors."""
    PercentageErrorQuery = '''
        SELECT to_char(totalerrorsperday.time,'FMMonth FMDD, YYYY'),
        cast(totalerrorsperday.errorsperday AS FLOAT)/
        cast(totalreqperday.reqperday AS FLOAT)*100
        AS percent
        FROM totalreqperday JOIN totalerrorsperday ON
        totalreqperday.time = totalerrorsperday.time
        ORDER BY percent DESC
    '''
    conn = psycopg2.connect(database=DBNAME)
    cursor = conn.cursor()
    cursor.execute(PercentageErrorQuery)
    results = cursor.fetchall()
    print("")
    print("Date(s) of where more than 1% of requests led to errors:")
    print("")

    for i in range(len(results)):
        date = results[i][0]
        errorpercent = results[i][1]
        if errorpercent >= 1:
            print("%s -- %d" % (date, errorpercent)+'%')

    conn.close()

    return results


# Run the program.
if __name__ == "__main__":
    top3articles()
    topAuthors()
    PercentageErrorDates()
