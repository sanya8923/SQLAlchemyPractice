from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert, select, delete, ForeignKey

engine = create_engine('sqlite:///your_database.db')
metadata = MetaData()

table_data1 = Table('table_data1',
                    metadata,
                    Column('user_id', Integer, primary_key=True),
                    Column('first_name', String(255)),
                    Column('last_name', String(255)),
                    Column('phone', String(255))
                    )

table_users1 = Table('table_users1',
                     metadata,
                     Column('user_id', Integer, ForeignKey('table_data1.user_id'), nullable=False),
                     Column('id', Integer, primary_key=True),
                     Column('first_name', String(255)),
                     Column('last_name', String(255))
                     )

table_contacts = Table('table_contacts',
                       metadata,
                       Column('user_id', Integer, ForeignKey('table_data1.user_id'), nullable=False),
                       Column('phone', String(255))
                       )

metadata.create_all(engine)


