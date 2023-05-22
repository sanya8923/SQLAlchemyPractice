from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert, select, delete

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
                     Column('user_id', Integer),
                     Column('id', Integer, primary_key=True),
                     Column('first_name', String(255)),
                     Column('last_name', String(255))
                     )

table_contacts = Table('table_contacts',
                       metadata,
                       Column('user_id', Integer),
                       Column('phone', String(255))
                       )

metadata.create_all(engine)

data = [
    {'first_name': 'Anton', 'last_name': 'Lapenko', 'phone': '89504387625'},
    {'first_name': 'Stiven', 'last_name': 'Spilberg', 'phone': '89234387620'},
    {'first_name': 'Nicolas', 'last_name': 'Kage', 'phone': '89604387618'},
    {'first_name': 'Gas', 'last_name': 'Vansant', 'phone': '89184387612'},
    {'first_name': 'David', 'last_name': 'Linch', 'phone': '89504381982'},
    {'first_name': 'Arseniy', 'last_name': 'Tarkovski', 'phone': '89534387629'},
    {'first_name': 'Marlon', 'last_name': 'Brando', 'phone': '89634381672'},
    {'first_name': 'Martin', 'last_name': 'Scorseze', 'phone': '89634387619'},
]


def print_data(table):
    stmt_select_data_from_table_data1 = select(table)  # select data from table stmt

    with engine.connect() as conn:
        rows = conn.execute(stmt_select_data_from_table_data1)

        for row in rows:
            print(row)

        conn.commit()


def insert_to_table_data1(data_to_insert: list):
    stmt_delete = delete(table_data1)
    stmt_ins = insert(table_data1).values(data_to_insert)  # insert data to table stmt

    with engine.begin() as conn:
        conn.execute(stmt_delete)
        conn.execute(stmt_ins)

    conn.commit()


def insert_to_table_users1():
    stmt_delete = delete(table_users1)
    stmt_sel = select(table_data1.c.user_id, table_data1.c.first_name, table_data1.c.last_name)
    stmt_ins = table_users1.insert().from_select(['user_id', 'first_name', 'last_name'], stmt_sel)

    with engine.begin() as conn:
        conn.execute(stmt_delete)
        conn.execute(stmt_ins)

    conn.commit()


def insert_to_table_contacts():
    stmt_delete = delete(table_contacts)
    stmt_sel = select(table_data1.c.user_id, table_data1.c.phone)
    stmt_ins = table_contacts.insert().from_select(['user_id', 'phone', ], stmt_sel)

    with engine.begin() as conn:
        conn.execute(stmt_delete)
        conn.execute(stmt_ins)

    conn.commit()


def search_full_name_by_phone_via_where(phone_for_search: str):
    stmt_sel_user_id = select(table_contacts.c.user_id) \
        .where(table_contacts.c.phone == f'{phone_for_search}') \
        .scalar_subquery()
    stmt_sel_full_name = select(table_users1.c.first_name, table_users1.c.last_name) \
        .where(table_users1.c.user_id == stmt_sel_user_id)

    with engine.connect() as conn:
        result = conn.execute(stmt_sel_full_name)

        gen_result = ''

        for row in result:
            for item in row:
                gen_result = gen_result + ' ' + item

        print(gen_result.strip())


def search_full_name_by_phone_via_filter_by(phone_for_search: str):
    stmt_sel_user_id = select(table_contacts.c.user_id)\
        .filter_by(phone=f'{phone_for_search}')\
        .scalar_subquery()
    stmt_sel_f_name = select(table_users1.c.first_name, table_users1.c.last_name)\
        .where(table_users1.c.user_id == stmt_sel_user_id)

    with engine.connect() as conn:
        result_proxy = conn.execute(stmt_sel_f_name)
        result = result_proxy.fetchall()

    gen_result = ''

    for row in result:
        for item in row:
            gen_result = gen_result + ' ' + item

    print(gen_result.strip())


insert_to_table_data1(data)

insert_to_table_users1()
# print_data(table_users1)

insert_to_table_contacts()
# print_data(table_contacts)

# search_full_name_by_phone_via_where('89634387619')
search_full_name_by_phone_via_filter_by('89634387619')
