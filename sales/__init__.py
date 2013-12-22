import os

from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sales.models import initialize_sql
from views.home import home_view 
from views.sales_month import sales_month_view

def db(request):
    maker = request.registry.dbmaker
    session = maker()

    def cleanup(request):
        session.close()
    request.add_finished_callback(cleanup)

    return session

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.scan('sales.models')
    if 'DATABASE_URL' in os.environ:
        enging = create_engine(os.environ['DATABASE_URL'])
    else:
        engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config.registry.dbmaker = sessionmaker(bind=engine)
    config.add_request_method(db, reify=True)
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_view(home_view, route_name='home', renderer='sales_month.mak')
    config.add_route('sales_month', '/sales_month')
    config.add_view(sales_month_view, route_name='sales_month', renderer='json')
    return config.make_wsgi_app()
