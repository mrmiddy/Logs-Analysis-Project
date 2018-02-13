#
# UDACITY Project 3 - Logs Analysis Project README

# Program Overview

The following files have been built to create an internal reporting tool program
that uses information from a mock newspaper database to display what kind of articles the newspaper site's readers like.

The database contains newspaper articles, as well as the web server log for the
site. The log has a database row for each time a reader loaded a web page.
Using that information, the program answers questions about the site's user
activity.

The program for this project's requirement runs from the command line. It does
not take any input from the user. Instead, it connects to the database, uses SQL queries to analyze the log data, and prints out the answers to the following questions:

1. What are the most popular three articles of all time, as in which articles have
been accessed the most? This information is presented as a sorted list with the
most popular article at the top.

Example:

> "Princess Shellfish Marries Prince Handsome" — 1201 views
> "Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
> "Political Scandal Ends In Political Scandal" — 553 views

2. Who are the most popular article authors of all time? That is, when summing
up all of the articles each author has written, which authors get the most page views? This information is presented as a sorted list with the most popular
author at the top.

Example:

> Ursula La Multa — 2304 views
> Rudolf von Treppenwitz — 1985 views
> Markoff Chaney — 1723 views
> Anonymous Contributor — 1023 views

3. On which days did more than 1% of requests lead to errors? The log table
includes a column status that indicates the HTTP status code that the news site
sent to the user's browser.

Example:

> July 29, 2016 — 2.5% errors


# Required Files, SQL VIEWS, and Database

There is one main file and three SQL views included for this project.

> 1.	newspaper-stats.py: This program contains the python code & SQL queries
to generate the answers to the three questions described in the
Program Overview. Some of the SQL queries rely on the SQL VIEWS listed in this
README file and are noted when the VIEWS are required.

The following SQL VIEWS are required to be run from the command line BEFORE
running the newspaper-stats.py file in order for the SQL queries in the newspaper-stats.py file to properly execute.

> 1.	SQL VIEW Name: log_path_num_nolimit : SQL query needed to be run at the
command line prior to program execution for the top3articles() function:

    create view log_path_num_nolimit AS SELECT path, count(*) AS num
        FROM log WHERE path != '/'
        GROUP BY path
        ORDER BY num DESC
        LIMIT 3;


> 2.	SQL VIEW Name: dateOf404s : SQL query needed to be run at the
command line prior to program execution for the PercentageErrorDates() function.

    create view dateOf404s AS SELECT time::timestamp::date, count(*) AS date404
        FROM log WHERE status != '200 OK'
        GROUP BY time
        ORDER BY date404 DESC;


> 3.	SQL VIEW Name: totalerrorsperday : SQL query needed to be run at the
command line prior to program execution for the PercentageErrorDates() function.

    create view totalreqperday AS SELECT time::timestamp::date,
        count(*) AS reqperday
        FROM log
        GROUP BY time::timestamp::date;

Required Database

Next, download the data here https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into your vagrant directory (which is shared with
your virtual machine) or similar program depending on the development
environment you are using.

Now load the site's data into your local database by: cd into the vagrant directory and use the command

> psql -d news -f newsdata.sql

Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.

The database includes three tables:

    The authors table includes information about the authors of articles.
    The articles table includes the articles themselves.
    The log table includes one entry for each time a user has accessed the site.


# Accessing/Opening the Project

Copy the file newspaper-stats.py in a directory where it can access the
database.  From your command line, run:

> python newspaper-stats.py

The program will run and will display the answers to questions one through three in the Program Overview.

# Credits

I have partially used and modified the instructions for this project from
UDACITY to assist with the README file for proper documentation.
