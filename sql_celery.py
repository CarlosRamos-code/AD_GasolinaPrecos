import sqlite3
import pandas as pd
from celery import Celery
import os
from datetime import timedelta

# Caminho absoluto do banco e CSV
base_dir = os.path.dirname(os.path.abspath(__file__))
db_caminho = os.path.join(base_dir, "gasolinaPrecos.db")
csv_files = ['CSV_gasolina_2000+.csv']

app = Celery("sql_celery", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

# Task a cada minuto
app.conf.beat_schedule = {'carregar-csv-10-por-vez': {'task': 'sql_celery.carregar_csv_10_por_vez','schedule': timedelta(minutes=1)}}

def renomeia_colunas(c):
    #Renomeia coluna para ser compatível com SQLite
    c = str(c) 
    c = c.replace(" ", "_").replace("-", "_")
    if c and c[0].isdigit():
        c = f"col_{c}"
    return c

@app.task(name="sql_celery.carregar_csv_10_por_vez")
def carregar_csv_10_por_vez():

    #import pdb; pdb.set_trace() # --> debug breakpoint
    conn = None
    try:
        conn = sqlite3.connect(db_caminho)
        tamanho_bloco = 10

        for arquivo in csv_files:
            arquivo_caminho = os.path.join(base_dir, arquivo)

            # Verifica se a tabela existe
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data'")
            tabela_existe = cursor.fetchone() is not None 

            #import pdb; pdb.set_trace() # --> segundo debug breakpoint
            if tabela_existe:
                cursor.execute("SELECT COUNT(*) FROM data")
                linhas_existentes = cursor.fetchone()[0]
            else:
                linhas_existentes = 0

            # Lê o próximo bloco do CSV
            df = pd.read_csv(arquivo_caminho,sep=',',decimal='.',index_col=0,
                skiprows=lambda x: x != 0 and x <= linhas_existentes,  # pula linhas já lidas, mas não o cabeçalho
                nrows=tamanho_bloco
            )

            if df.empty:
                continue

            df.index.name = 'index_name'

            #import pdb; pdb.set_trace() # --> terceiro debug breakpoint
            if not tabela_existe:
                df.to_sql('data', conn, if_exists='replace', index_label='index_name')
            else:
                # Pega colunas existentes no banco
                cursor.execute("PRAGMA table_info(data)")
                colunas_existentes = [col[1] for col in cursor.fetchall()]

                # Insere os dados
                df.to_sql('data', conn, if_exists='append', index_label='index_name')

    except Exception as e:
        raise e
