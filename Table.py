import sqlite3

def create_tables():
    conobj = sqlite3.connect(database="bank.sqlite")
    curobj = conobj.cursor()
    query = """create table if not exists accounts(
    acn integer primary key autoincrement,
    name text,
    pass text,
    bal float,
    mob text,
    adhar text,
    email text,
    opendate datetime
    )
    """
    curobj.execute(query)
    conobj.close()
    print("Table created or exists")