import sqlite3
import pandas as pd

#conectando ao banco
con = sqlite3.connect("mydata.sqlite")

# criar tabela\
con.execute("""
CREATE TABLE IF NOT EXISTS test (
    id INTERGER,
    nome TEXT
)
""")

#inserir dados
con.execute("INSERT INTO test(id,nome) VALUES (1, 'Larson')")
con.execute("INSERT INTO test(id,nome) VALUES (2, 'Th')")

#salvando alteracoes
con.commit()

#consultar dados
cursor = con.execute("SELECT * FROM test")
rows = cursor.fetchall()

#converter para DataFrame
df = pd.DataFrame(rows, columns=[x[0] for x in cursor.description])

print(df)
#fechar conexao
con.close()