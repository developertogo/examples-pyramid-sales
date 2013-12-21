from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from sales.models import DBSession
from sales.models.sales_month import SalesMonth

# fetch and return data from db
def sales_month_view(request):
    try:
        data = []
        rs = DBSession.query(SalesMonth).order_by(SalesMonth.created.desc()).all()
        for row in rs:
            data.append({'month': row.created.strftime('%b-%y'), 'sales': row.amount})
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return data

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_sales_db" script
@view_config(route_name='sales_month', renderer='json')
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

