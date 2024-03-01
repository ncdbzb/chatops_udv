from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from src.auth.models import user


metadata = MetaData()

doc = Table(
    "doc",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, unique=True, nullable=False),
    Column("description", String, nullable=False),
    Column("path", String, nullable=False),
    Column("user_id", Integer, ForeignKey(user.c.id)),
)
