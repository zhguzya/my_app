from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE_NAME_ORM, DATABASE_NAME_USERS

#mikrotik_db
BaseMikrotik = declarative_base()
engine_mikrotik = create_engine(f'sqlite:///{DATABASE_NAME_ORM}', echo=True) # унести в config
SessionMikrotik = sessionmaker(bind=engine_mikrotik)

#users_db
BaseUsers = declarative_base()
engine_users = create_engine(f'sqlite:///{DATABASE_NAME_USERS}', echo=True)
SessionUsers = sessionmaker(bind=engine_users)