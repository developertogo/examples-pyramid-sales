examples-python-pyramid-sales
=============================

d3.js linear graph of 'Sales over Month' data fetched from a web server running Pyramid with SQLAlchemy connected to a mySQL DB.

Sales over Month App - README
=============================

Objective
---------

Demonstrate understanding of the working in/out's of the Python Pyrarmid Web Framework with SQLAlchemy.

Project
-------

Display a linear graph of sales over time (y-axis is $, x-axis is month).
Create dummy/static data, but load the data via an ajax call.

Strategy
--------

* Select an elegant front end graphic library
* Data is randomly auto-generated and stored in the DB
* Data will be fetched from DB and pass to the front end for display
* Unit test the workflow
* Setup Pyramid directory structure for models and views so that new functionality is easily added

Getting Started
---------------

Note: $venv = <your virtual env>

- cd <directory containing this file>

# install require packages
- $venv/bin/python setup.py develop

# initialize the db creating a 'sales_month' table if it does not exist
# and inserting random values
- $venv/bin/initialize_sales_db development.ini

# run the unitest
- $venv/bin/python setup.py test -q

# start app
- $venv/bin/pserve development.ini

Using d3.js to display the sales-month line graph
