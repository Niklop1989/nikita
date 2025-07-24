from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from nikita.src.database import Base


class Recipes(Base):
    __tablename__ = 'recipes'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    time_to_cook: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String)
    views: Mapped[int] = mapped_column(Integer, default=0)
