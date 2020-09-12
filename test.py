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