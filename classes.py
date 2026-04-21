from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, Annotated
from database import Base
from datetime import datetime
from pydantic import BaseModel

intpk = Annotated[int, mapped_column(primary_key=True)]

# Группы
class Categories(Base):
    __tablename__ = 'categories'
    
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(100))

    is_default: Mapped[bool] = mapped_column(Boolean, default=False) 
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'), nullable=True)  
    
    exercises = relationship("Exercises", back_populates="category")
    user = relationship("Users", back_populates="custom_categories")
    
# Упражнения
class Exercises(Base):
    __tablename__ = 'exercises'
    
    id: Mapped[intpk]
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    name: Mapped[str] = mapped_column(String(100))
    image_filename: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    is_default: Mapped[bool] = mapped_column(Boolean, default=False)  
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'), nullable=True) 

    category = relationship("Categories", back_populates="exercises")
    exercises_users = relationship("Exercises_Users", back_populates="exercise")
    user = relationship("Users", back_populates="custom_exercises")
    exercise_stats = relationship("Exercise_Stats", back_populates="exercise")

# Пользовательские упражнения
class Exercises_Users(Base):
    __tablename__ = 'exercises_users'
    
    id: Mapped[intpk]
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    exercise_id: Mapped[int] = mapped_column(ForeignKey('exercises.id'))

    notes: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user = relationship("Users", back_populates='exercises_users')
    exercise = relationship("Exercises", back_populates="exercises_users")
    
# Пользователи
class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())

    exercises_users = relationship("Exercises_Users", back_populates='user')
    custom_categories = relationship("Categories", back_populates='user')
    custom_exercises = relationship("Exercises", back_populates='user')
    exercise_stats = relationship("Exercise_Stats", back_populates='user')
    
# Статистика упражнений
class Exercise_Stats(Base):
    __tablename__ = 'exercise_stats'
    
    id: Mapped[intpk]
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    exercise_id: Mapped[int] = mapped_column(ForeignKey('exercises.id'), nullable=False)
    
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)  
    weight: Mapped[int] = mapped_column(Integer, nullable=False)  
    approach: Mapped[int] = mapped_column(Integer, nullable=False) 
    
    # Отношения
    user = relationship("Users", back_populates='exercise_stats')
    exercise = relationship("Exercises", back_populates="exercise_stats")  

    
# Модели данных
class UserExerciseCreate(BaseModel):
    category_name: str
    exercise_name: str
    image_filename: Optional[str] = "default_exercise.jpg"
    
class UserExerciseStatsCreate(BaseModel):
    exercise_id: int
    date: datetime
    weight: int
    approach: int
    
    
    
    
