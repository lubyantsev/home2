from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Определение URL базы данных
DATABASE_URL = 'sqlite:///taskmanager.db'

# Создание движка
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создание локальной сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базового класса
Base = declarative_base()