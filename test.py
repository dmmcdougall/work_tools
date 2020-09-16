# Python code to initialize a dictionary
# with only keys from a list
import pandas as pd
import config as cfg

# List of keys
keyList = ["Paras", "Jain", "Cyware"]

# initialize dictionary
d = {}

# iterating through the elements of list
for i in keyList:
    d[i] = None

print(d)

# Creating an empty Dataframe with column names only
dfObj = pd.DataFrame(columns=['User_ID', 'UserName', 'Action'])

#ODBC supports parameters using a question mark as a place holder in the SQL. You provide the values for the question marks by passing them after the SQL:
# cursor = cfg.conn.cursor()
# cursor.execute("""
#     select user_id, user_name
#       from users
#      where last_logon < ?
#        and bill_overdue = ?
# """, datetime.date(2001, 1, 1), 'y')



# # find the number we need to start the new data with
# query = "SELECT * FROM HeadShiftWorkedTable"
# df_hShift = pd.read_sql(query, cfg.conn)
# last_shift = df_hShift['HeadShiftWorkedID'].max()
# print(last_shift) # for testing

# find the number we need to start the new data with
def find_next_row_from_db(my_table, my_column):
    query = ("""
        declare @tablename varchar(50) 
        set @tablename = my_table 
        declare @sql varchar(500)
        set @sql = 'select * from ' + @tablename 
        exec (@sql)
    """"    )

    df_hShift = pd.read_sql(query, cfg.conn)
    last_shift = df_hShift[my_column].max()
    # print(last_shift) # for testing
    new_shift = last_shift + 1
    return new_shift

table = "HeadShiftWorkedTable"
column = "HeadShiftWorkedID"

find_next_row_from_db(table, column)

