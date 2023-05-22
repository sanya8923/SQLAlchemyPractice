from sqlalchemy import select, func, cast, text, literal_column, literal
from insert_examples import table, engine
#
# # The select() SQL Expression Construct
#
# stmt = select(table).where(table.c.name == 'Masha')
# print(f'output 1 SELECT SQL Expression Construct from WHERE: \n{stmt}\n')
#
# # with engine.connect() as conn:
# #     for row in conn.execute(stmt):
# #         print(row)
#
# # Setting the COLUMNS and FROM clause
#
# stmt = select(table.c.name)
# print(f'output 2 SELECT SQL Expression Construct ONLY name (var.1): \n{stmt}\n')
#
# # with engine.connect() as conn:
# #     for row in conn.execute(stmt):
# #         print(row)
#
# stmt = select(table.c['name', 'age'])
# print(f'output 3 SELECT SQL Expression Construct ONLY name (var.2): \n{stmt}\n')
#
# # with engine.connect() as conn:
# #     for row in conn.execute(stmt):
# #         print(row)
#
# # Selecting from Labeled SQL Expressions
#
# stmt = select(('Username: ' + table.c.name).label('username')).order_by(table.c.name)
# print(f'output 4 Selecting from Labeled SQL Expressions: \n{stmt}\n')
#
# # with engine.connect() as conn:
# #     for row in conn.execute(stmt):
# #         print(row.username)
#
# # Selecting with Textual Column Expressions
#
# stmt = select(text("'some phrase'"), table.c.name).order_by(table.c.name)
# # ошибка, не добавляет подпись как в прошлом примере, а создает столбик some phrase  со значением None
# print(f'output 5 Selecting with text: \n{stmt}\n')
#
# # with engine.connect() as conn:
# #     print(conn.execute(stmt).all())
#
# stmt = select(literal_column("'some phrase'").label('p'), table.c.name).order_by(table.c.name)
# print(f'output 6 Selecting with literal_column: \n{stmt}\n')
# # а вот этот способ работает (literal_column используется для создания идентификатора столбца)
# # with engine.connect() as conn:
# #     for row in conn.execute(stmt):
# #         print(f'{row.p} {row.name}')
#
# stmt = select(literal("'some phrase'").label('p'), table.c.name).order_by(table.c.name)
# print(f'output 7 Selecting with literal: \n{stmt}\n')
# # тоже работает
# # with engine.connect() as conn:
# #     for row in conn.execute(stmt):
# #         print(f'{row.p} {row.name}')
#
# # The WHERE clause
#
# print(f"output 8 Using boolean expressions: \n{table.c.name == 'Masha'}\n")
# # "table".name = :name_1
#
stmt = select(table.c.age).where(table.c.name == 'Gosha')
print(f"output 9 Selecting WHERE using boolean: \n{stmt}\n")

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)

