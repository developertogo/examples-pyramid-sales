import calendar
import datetime
import math
import os
import random
import sys
import transaction

from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from sales.models import DBSession
from sales.models import Base
from sales.models import initialize_sql
from sales.models.sales_month import SalesMonth

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

# add a month to a date
def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)

# return delta month from a date
def month_delta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31, \
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    config = Configurator(settings=settings)
    config.scan('sales.models')
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)

    # truncate 'sales_month' table if it exists
    connection = DBSession.connection()
    if engine.dialect.has_table(connection, 'sales_month'): 
        DBSession.execute('truncate sales_month')
        DBSession.commit()

    somedate = datetime.date.today()
    with transaction.manager:
        # insert static dummy data
        for m in range(-12, 1):
            amount = math.ceil(random.uniform(0.00, 1000.00) * 100) / 100
            prev_month_date = month_delta(somedate, m)
            sales_month = SalesMonth(amount = amount, created = prev_month_date)
            DBSession.add(sales_month)
            DBSession.commit()
