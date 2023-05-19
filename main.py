from sqlalchemy import create_engine, Integer, String, ForeignKey, insert
from sqlalchemy.orm import Session, DeclarativeBase, mapped_column

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
session = Session(engine)


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users_table'
    id = mapped_column(Integer(), primary_key=True)
    name = mapped_column(String(255))


class Data(Base):
    __tablename__ = 'users_data_table'
    id = mapped_column(Integer(), primary_key=True)
    user_id = mapped_column(Integer(), ForeignKey('users_table.id'), nullable=False)
    rule = mapped_column(String(255))
    age = mapped_column(String(255))
    work = mapped_column(String(255))


Base.metadata.create_all(engine)


class OriginData:
    @staticmethod
    def original_data():
        users_data = [dict(name='Anton', rule='parent', age='23', work='proger'),
                      dict(name='Sveta', rule='child', age='23', work='tester'),
                      dict(name='Dima', rule='parent', age='23', work='buyer'),
                      dict(name='Sasha', rule='child', age='23', work='seller'),
                      dict(name='Kirril', rule='parent', age='23', work='blogger'),
                      dict(name='Vadim', rule='child', age='23', work='taxer')
                      ]
        return users_data


class DataHandler:
    data = []

    user_id = None
    data_id = None

    name = None
    rule = None
    age = None
    work = None

    def __init__(self, *args):
        self.data = args


class DataSeparator(DataHandler):

    def data_separator(self):
        try:
            users_db = Users()
            for line in self.data:
                for item in line:
                    stmt = insert(users_db).values(name=item.name)
                    print(stmt)
        except Exception as e:
            raise e
            session.rollback()
        finally:
            session.close()


users = Users()
sep = DataSeparator(OriginData.original_data())

