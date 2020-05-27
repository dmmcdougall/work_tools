'''

'''

# standard library
import pyodbc

# third part libraries

# local repo

# read from SQL and print to screen
def read(query, conn):
    print("Read Method")
    cursor = conn.cursor()
    cursor.execute(query)
    for row in cursor:
        print(row)
    print

# read from SQL without printing
def read2(query, conn):
    print("Read Method")
    cursor = conn.cursor()
    cursor.execute(query)

# delete data from anSQL table
def general(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)


# does your table exist?
def tblexists(table_name, conn):
    cursor = conn.cursor()
    if cursor.tables(table=table_name, tableType='TABLE').fetchone():
        print("exists")
    else:
        print("doesn't exist")

def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False


# not tested
def read_db2df(query, conn):
    print("Read Method")
    cursor = conn.cursor()
    cursor.execute(query)
    for row in cursor:
        print(row)
    print


# not tested
def create(conn):
    print("Create")
    cursor = conn.cursor()
    cursor.execute(
        'insert into dummy(a,b) values(?,?);',
        (3232, 'catzzz')
    )
    conn.commit()
    read(conn)


# not tested
def update(conn):
    print("Update")
    cursor = conn.cursor()
    cursor.execute(
        'update dummy set = ? where a = ?;',
        ('dogzzz', 3232)
    )
    conn.commit()
    read(conn)


# not tested
# def delete2(conn, query):
#     print("Delete")
#     cursor = conn.cursor()
#     cursor.execute(
#         'delete from <tblname dummy a > 5;',
#     )
#     conn.commit()
#     read(conn)


if __name__ == '__main__':
    print()
    print('------------')
    print("METHOD CHECK")
    print('------------')
    print()
    conn = pyodbc.connect(
        "Driver={ODBC Driver 13 for SQL Server};"
        "Server=CGYSQL01\MISC;"
        "Database=production;"
        "Trusted_Connection=yes;"
    )
    query = "SELECT * FROM sys.tables"
    read(query, conn)


