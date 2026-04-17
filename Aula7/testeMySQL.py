import mysql.connector

config = {
    'user': 'Eduardo',
    'password': 'Eduardo*12',
    'host': 'localhost',
    'database': 'meu_banco'
}

cnx = mysql.connector.connect(**config)

print("deu bom")

cnx.close()