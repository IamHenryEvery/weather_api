from bestconfig import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


config = Config("config.ini", exclude_default=True)
engine = create_engine(
    f"sqlite:///{config['Database']['dbname']}",
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
