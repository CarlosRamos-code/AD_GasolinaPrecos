import sqlite3
import pandas as pd
from celery import Celery
import logging
import os

# Definindo caminho absoluto do banco
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "gasolinaPrecos.db")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379")

#definindo função para o celery poder executar
@app.task
def carregar_csv():
    logging.info("Iniciando tarefa carregar_csv")
    try:
        logging.info(f"Salvando dados no SQLite em: {db_path}")
        conn = sqlite3.connect(db_path)
        logging.info("Conexão com SQLite aberta")

        # Carregar CSVs
        df_2000 = pd.read_csv(os.path.join(base_dir, 'CSV_gasolina_2000+.csv'), sep=',', decimal='.', index_col=0)
        df_2010 = pd.read_csv(os.path.join(base_dir, 'CSV_gasolina_2010+.csv'), sep=',', decimal='.', index_col=0)
        logging.info(f"CSV 2000: {df_2000.shape}, CSV 2010: {df_2010.shape}")

        # Concatenar
        df_gasolina = pd.concat([df_2000, df_2010])
        logging.info(f"DataFrames concatenados: {df_gasolina.shape}")

        # Salvar o SQL e fechar conexão
        df_gasolina.index.name = 'index_name'
        df_gasolina.to_sql('data', conn, index_label='index_name', if_exists='replace')
        conn.commit()
        logging.info("Dados salvos no SQLite com sucesso")

        conn.close()
        logging.info("Conexão com SQLite encerrada")
        return f"{df_gasolina.shape[0]} linhas inseridas no banco"
    
    #Definindo mensagem de erro
    except Exception as e:
        logging.error(f"Erro durante a execução da tarefa: {e}")
        raise e
