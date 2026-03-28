import sqlite3
import pandas as pd

con = sqlite3.connect("mydata.sqlite")

#seleciona rosas as colunas da tabela test
df = pd.read_sql_query("SELECT * FROM test", con)

print(df)

con.close()