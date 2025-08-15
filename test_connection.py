import os
import pyodbc

SERVER = os.getenv("DB_SERVER", "Seu_servidor_aqui")
DATABASE = os.getenv("DB_NAME", "Seu_banco_de_dados_aqui")
UID = os.getenv("DB_USER", "Seu_usuario_aqui")
PWD = os.getenv("DB_PASS", "sua_senha_aqui")

conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={UID};"
    f"PWD={PWD}"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
cursor.execute("SELECT TOP 5 * FROM dbo.Usuario")
for row in cursor.fetchall():
    print(row)
conn.close()