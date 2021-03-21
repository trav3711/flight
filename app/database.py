from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://dhxnhmqz:INAxHrxm3u0MEPzvlLV5B5Wd-X7GGdMt@kashin.db.elephantsql.com:5432/dhxnhmqz"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
