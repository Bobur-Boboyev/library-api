from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Date

from app.database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(length=100), nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    born_date: Mapped[date] = mapped_column(Date, nullable=True)

    books: Mapped[list["Book"]] = relationship(
        "Book", uselist=True, back_populates="author"
    )

    books: Mapped[List["Book"]] = relationship(back_populates="author")

    def __str__(self):
        return f"{self.id}. {self.full_name}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
