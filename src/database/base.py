import databases
import sqlalchemy
from pydantic import BaseModel

from src.settings.config import DATABASE_NAME

DATABASE_URL = f"sqlite:///{DATABASE_NAME}"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("tg_id", sqlalchemy.Integer),
    sqlalchemy.Column("full_name", sqlalchemy.String),
    sqlalchemy.Column("in_chat", sqlalchemy.Boolean, default=False)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class UserIn(BaseModel):
    full_name: str
    tg_id: int
    in_chat: bool


class UserUpdate(BaseModel):
    tg_id: int
    in_chat: bool


class UserOut(UserIn):
    id: int


async def add_user_db(user: UserIn):
    query = users.insert().values(full_name=user.full_name, tg_id=user.tg_id, in_chat=user.in_chat)
    result = await database.execute(query)
    return result


async def get_user_one_db(tg_id: int):
    return await database.fetch_one(users.select().where(users.c.tg_id == tg_id))


async def update_user_db(user: UserUpdate):
    query = users.update().where(users.c.tg_id == user.tg_id).values(in_chat=user.in_chat)
    result = await database.execute(query)
    return result
