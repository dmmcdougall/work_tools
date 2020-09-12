# Python code to initialize a dictionary
# with only keys from a list

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

cursor.execute("""
    select user_id, user_name
      from users
     where last_logon < ?
       and bill_overdue = ?
""", datetime.date(2001, 1, 1), 'y')