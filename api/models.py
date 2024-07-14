import sqlalchemy as sa
import sqlalchemy.orm as so
from database import Base


class Account(Base):
    __tablename__ = "account"

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    username: so.Mapped[str] = so.mapped_column(
        sa.String(20), unique=True, nullable=False
    )
    password: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String, unique=True, nullable=False)
