import unittest
import datetime
import math
import random
import transaction

from pyramid import testing
from sales.models import DBSession

class TestSalesMonth(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        # mysql config
        #engine = create_engine('mysql://admin:%2F8dm1n@localhost/sales')
        engine = create_engine('postgresql+psycopg2://root:root@localhost/sales')
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
