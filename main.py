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

# The insert() SQL Expression Construct

stmt1 = insert(table).values(name='Sasha', age=23, phone=89504398717)
print(f'output 1 (stmt1): \t\t\t\t\t\t\t{stmt1}')

compiled = stmt1.compile().params
print(f'output 2 Keys and Values (stmt1): \t\t\t{compiled}')

# Executing the Statement

with engine.connect() as conn:
    result = conn.execute(stmt1)

    print(f'output 3 Cursor position(stmt1): \t\t\t{result.inserted_primary_key}')
    conn.commit()

# INSERT usually generates the “values” clause automatically

print(f'\noutput 4 usually generates the “values” clause automatically \n{insert(table)}\n')

with engine.connect() as conn:
    result = conn.execute(
        insert(table).values
        (
            [
                {'name': 'Masha', 'age': 19, 'phone': 89234398717},
                {'name': 'Gosha', 'age': 32, 'phone': 89234391411}
            ]
        )
    )
    conn.commit()

# Scalar Method That Allows To Automatically Find The ID Of A User By His Username

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

print(f'output 5 Insert with scalar request:  \t\t{insert(user_accounts).values().compile(engine)}')

# INSERT ... RETURNING

insert_stmt = insert(user_accounts).returning(user_accounts.c.id, user_accounts.c.email)
print(f'output 6 INSERT ... RETURNING: \t\t\t\t{insert_stmt}')
print(f'output 7 INSERT ... RETURNING params: \t\t{insert_stmt.compile().params}')

select_stmt = select(user_accounts.c.id, user_accounts.c.name + "@aol.com")
insert_stmt = insert(user_accounts).from_select(
              ['id', 'email'], select_stmt)

print(f'\noutput 8 INSERT ... FROM SELECT:\n{insert_stmt.returning(user_accounts.c.id, user_accounts.c.email)}\n')

# INSERT…FROM SELECT

print(f'\noutput 9 INSERT ... FROM SELECT:\n{insert_stmt}\n')
