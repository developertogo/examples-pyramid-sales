import unittest
import datetime
import math
import random
import os
import transaction
import ConfigParser

from pyramid import testing
from sales.models import DBSession

class TestSalesMonth(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine

        database_url = ''
        if 'DATABASE_URL' in os.environ:
            database_url = os.environ['DATABASE_URL']
        else:
            # get sqlalchemy url var      
            basePath = '.'
            configurationPath = 'development.ini'
            defaultByKey = {'here': basePath}
            configParser = ConfigParser.ConfigParser(defaultByKey)
            if not configParser.read(configurationPath):
                raise ConfigParser.Error('Could not open %s' % configurationPath)
            settings = {}
            for key, value in configParser.items('app:main'):
                if 'sqlalchemy.url' == key:
                    settings[key] = value
            database_url = settings['sqlalchemy.url']
        engine = create_engine(database_url)

        from sales.models import Base
        from sales.models.sales_month import SalesMonth
        from sales.models import initialize_sql
        initialize_sql(engine)
        with transaction.manager:
            amount = math.ceil(random.uniform(0.00, 1000.00) * 100) / 100
            today = datetime.date.today()
            model = SalesMonth(amount=amount, created=today)
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_sales_month(self):
        from views.sales_month import sales_month_view
        request = testing.DummyRequest()
        data = sales_month_view(request)
        self.assertTrue(data[0]['month'] != '')
        self.assertTrue(data[0]['sales'] >= 0)
