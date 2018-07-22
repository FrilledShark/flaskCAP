import os

from peewee import *

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'database.db')

db = SqliteDatabase(filename)


class BaseModel(Model):
    class Meta:
        database = db


# Used for domain control
class Domain(BaseModel):
    domain_name = CharField(unique=True)
    password = CharField()
    date = DateTimeField()


#
# Tables
#

class User(BaseModel):
    domain = ForeignKeyField(Domain, backref="users", null=True)
    username = CharField(unique=True)
    password = CharField()


class Coin(BaseModel):
    user = ForeignKeyField(User, backref="coins")
    coin = CharField()
    address = CharField(null=True)


tables = [User, Coin, Domain]


if __name__ == "__main__":
    db.create_tables(tables)
