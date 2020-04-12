import orm
import databases
import sqlalchemy

from options import DATABASE_NAME


database = databases.Database(f"sqlite:///{DATABASE_NAME}")
metadata = sqlalchemy.MetaData()


class Language(orm.Model):
    __metadata__ = metadata
    __database__ = database
    __tablename__ = "languages"

    id = orm.Integer(primary_key=True)
    name = orm.String(max_length=3)


class Combination(orm.Model):
    __metadata__ = metadata
    __database__ = database
    __tablename__ = "combinations"

    id = orm.Integer(primary_key=True)
    name = orm.Text()
    language = orm.ForeignKey(Language)


class Good(orm.Model):
    __metadata__ = metadata
    __database__ = database
    __tablename__ = "goods"

    id = orm.Integer(primary_key=True)
    name = orm.Text()
    product_url = orm.Text()
    image_url = orm.Text()
    price = orm.Text()
    combination = orm.ForeignKey(Combination)

# Create the database
engine = sqlalchemy.create_engine(str(database.url))
metadata.create_all(engine)
