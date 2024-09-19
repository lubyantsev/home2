from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.backend.db import Base
from sqlalchemy.schema import CreateTable

class User(Base):
    __tablename__ = 'users'  # Используйте двойные подчеркивания для имени таблицы
    __table_args__ = {'extend_existing': True}  # Позволяет переопределить таблицу

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    slug = Column(String, unique=True, index=True)

    # Связь с моделью Task
    tasks = relationship("Task", back_populates="user")  # Убедитесь, что Task определен где-то еще

# Для вывода SQL-команды создания таблицы User
print(CreateTable(User.__table__))