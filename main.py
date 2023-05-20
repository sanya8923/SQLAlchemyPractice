from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert
from sqlalchemy import select, bindparam

engine = create_engine('sqlite:///your_database.db')
metadata = MetaData()

table = Table('table', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(255)),
              Column('age', Integer()),
              Column('phone', Integer())
              )

metadata.create_all(engine)

stmt1 = insert(table).values(name='Sasha', age=23, phone=89504398717)
print(f'output 1 (stmt1): \t\t\t\t\t\t\t{stmt1}')

compiled = stmt1.compile().params
print(f'output 2 Keys and Values (stmt1): \t\t\t{compiled}')

with engine.connect() as conn:
    result = conn.execute(stmt1)

    print(f'output 3 Cursor position(stmt1): \t\t\t{result.inserted_primary_key}')
    conn.commit()

stmt2 = insert(table)

with engine.connect() as conn:
    result = conn.execute(
             insert(table),
             [
                 {'name': 'Masha', 'age': 19, 'phone': 89234398717},
                 {'name': 'Gosha', 'age': 32, 'phone': 89234391411}
             ]
    )
    print(f'output 4 (stmt2): \t\t\t\t\t\t\t{result}')
    conn.commit()

user_accounts = Table('user_account_table', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String(255)),
                      Column('email', String(255))
                      )

metadata.create_all(engine)

scalar_subq = (
    select(user_accounts.c.id)
    .where(user_accounts.c.name == bindparam("username"))
    .scalar_subquery()
)

with engine.connect() as conn:
    result = conn.execute(
        insert(user_accounts).values(id=scalar_subq),
        [
            {"username": "spongebob", "email_address": "spongebob@sqlalchemy.org"},
            {"username": "sandy", "email_address": "sandy@sqlalchemy.org"},
            {"username": "sandy", "email_address": "sandy@squirrelpower.org"},
        ],
    )
    conn.commit()

print(f'output 5: {insert(user_accounts).values().compile(engine)}')

