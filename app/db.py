from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import psycopg2
from app.config import settings

# conn_string = "host='db' dbname='postgres' user='postgres' password='password'"
#
# connection = psycopg2.connect(conn_string)
# connection.close()

Base = declarative_base()

engine = create_engine(
    settings.DB_DSN,
)

Session = sessionmaker(bind=engine)
