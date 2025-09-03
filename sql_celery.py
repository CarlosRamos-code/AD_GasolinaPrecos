import sqlite3
import pandas as pd
from celery import Celery
import logging

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuração do Celery
app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379"
)

@app.task
def carregar_csv():
    logging.info("Iniciando tarefa carregar_csv")
    try:
        # Conecta no banco SQLite
        conn = sqlite3.connect("gasolinaPrecos.db")
        logging.info("Conexão com SQLite aberta")

        # Carrega CSVs
        df_2000 = pd.read_csv('CSV_gasolina_2000+.csv', sep=',', decimal='.', index_col=0)
        logging.info(f"CSV 2000 carregado: {df_2000.shape}")

        df_2010 = pd.read_csv('CSV_gasolina_2010+.csv', sep=',', decimal='.', index_col=0)
        logging.info(f"CSV 2010 carregado: {df_2010.shape}")

        # Concatena os DataFrames
        df_gasolina = pd.concat([df_2000, df_2010])
        logging.info(f"DataFrames concatenados: {df_gasolina.shape}")

        # Salva no SQLite
        df_gasolina.index.name = 'index_name'
        df_gasolina.to_sql('data', conn, index_label='index_name', if_exists='replace')
        logging.info("Dados salvos no SQLite com sucesso")

        conn.close()
        logging.info("Conexão com SQLite encerrada")

    except Exception as e:
        logging.error(f"Erro durante a execução da tarefa: {e}")
        raise e
