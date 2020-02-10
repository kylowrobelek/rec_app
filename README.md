# rec_app

API is based on Flask framework. There is celery task which fetches data every midnight from espn.

This api provides three endpoints:

GET /dates - returns all dates of scores fetch so far

GET /score/actual - returns actual scores basing on last date

GET /score/date/?date=<some_date> - returns scores basing on provided date (e.g. fetch from /dates)

There are also 4 unittests provided.
