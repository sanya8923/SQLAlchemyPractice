from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select, ForeignKey, func

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
                     Column('user_id', Integer, ForeignKey('table_contacts.user_id'), nullable=False),
                     Column('id', Integer, primary_key=True),
                     Column('first_name', String(255)),
                     Column('last_name', String(255))
                     )

table_contacts = Table('table_contacts',
                       metadata,
                       Column('user_id', Integer, primary_key=True),
                       Column('phone', String(255))
                       )

metadata.create_all(engine)


def print_users_data_via_join_from():
    stmt = select(table_users1.c.first_name, table_contacts.c.phone).join_from(table_users1, table_contacts)

    gen_result = ''

    with engine.connect() as conn:
        result_proxy = conn.execute(stmt)
        result = result_proxy.fetchall()

    for row in result:
        for item in row:
            gen_result = gen_result + ' ' + item

    conn.commit()

    print(gen_result.strip())


def print_users_data_via_join():
    stmt = select(table_users1.c.last_name, table_contacts.c.phone).join(table_users1)

    gen_result = ''

    with engine.connect() as conn:
        result_proxy = conn.execute(stmt)
        result = result_proxy.fetchall()

        conn.commit()

    for row in result:
        for item in row:
            gen_result = gen_result + ' ' + item

    print(gen_result.strip())


def print_users_data_via_join_and_select_from():
    stmt = select(table_users1.c.last_name, table_contacts.c.phone).select_from(table_users1).join(table_contacts)

    gen_result = ''

    with engine.connect() as conn:
        result_proxy = conn.execute(stmt)
        result = result_proxy.fetchall()

        conn.commit()

    for row in result:
        for item in row:
            gen_result = gen_result + ' ' + item

    print(gen_result.strip())


def count_row():
    stmt = select(func.count('*')).select_from(table_users1)

    gen_result = ''

    with engine.connect() as conn:
        result_proxy = conn.execute(stmt)
        result = result_proxy.fetchall()

        conn.commit()

    for row in result:
        for item in row:
            gen_result = item

    print('Number rows ' + str(gen_result))


# print_users_data_via_join_from()
# print_users_data_via_join()
# print_users_data_via_join_and_select_from()
count_row()
