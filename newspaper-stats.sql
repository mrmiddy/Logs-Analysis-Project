CREATE VIEW log_path_num_nolimit AS SELECT path, count(*) AS num
    FROM log WHERE path != '/'
    GROUP BY path
    ORDER BY num DESC
    LIMIT 3;

CREATE VIEW dateOf404s AS SELECT time::timestamp::date, count(*) AS date404
    FROM log WHERE status != '200 OK'
    GROUP BY time
    ORDER BY date404 DESC;

CREATE VIEW totalerrorsperday AS SELECT time, count(*) AS errorsperday
    FROM dateOf404s
    GROUP BY time;

CREATE VIEW totalreqperday AS SELECT time::timestamp::date,
    count(*) AS reqperday
    FROM log
    GROUP BY time::timestamp::date;
