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


def print_users_data_via_join_from():
    stmt = select(table_users1.c.first_name, table_data1.c.phone).join_from(table_users1, table_data1)

    gen_result = ''

    with engine.connect() as conn:
        result_proxy = conn.execute(stmt)
        result = result_proxy.fetchall()

        for row in result:
            for item in row:
                gen_result = gen_result + ' ' + item

    conn.commit()

    print(gen_result.strip())


print_users_data_via_join_from()
