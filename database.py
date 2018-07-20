from datetime import datetime
from peewee import *
import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'database.db')

db = SqliteDatabase(filename)


class BaseModel(Model):
    class Meta:
        database = db

#
# Tables
#


class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()


class Coin(BaseModel):
    user = ForeignKeyField(User, backref="coins")
    coin = CharField()
    address = CharField(null=True)


tables = [User, Coin]


if __name__ == "__main__":
    db.create_tables(tables)
