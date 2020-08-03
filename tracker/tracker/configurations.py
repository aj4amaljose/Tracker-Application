"""
Sets application configurations
"""
import os

POI_APP_PORT = os.environ['POI_APP_PORT'] if 'POI_APP_PORT' in os.environ else '80'
pg_user = os.environ['POSTGRES_USER']
pg_password = os.environ['POSTGRES_PASSWORD']
pg_database = os.environ['POSTGRES_DB']
pg_host_name = os.environ['POSTGRES_SERVICE'] \
    if 'POSTGRES_SERVICE' in os.environ else 'localhost'
pg_port = os.environ['POSTGRES_PORT']

POI_PG_DB_CONNECTION = "postgresql://{}:{}@{}:{}/{}".format(
    pg_user, pg_password, pg_host_name, pg_port, pg_database)
