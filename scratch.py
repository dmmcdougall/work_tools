import pandas as pd
import db_functions as dbfnc
import config as cfg
from datetime import date

value_to_check = pd.Timestamp((date.today().year-2), date.today().month, date.today().day)

print(value_to_check)