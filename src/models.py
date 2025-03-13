from sqlalchemy import Column, String, Integer

from .database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True) #
    cooking_time = Column(Integer, nullable=False) #
    count_of_view = Column(Integer, default=0)
    ingredients = Column(String, nullable=False)
    description = Column(String)