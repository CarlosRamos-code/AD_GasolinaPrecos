import sqlite3
import pandas as pd
import os

# Caminho absoluto do banco 
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "gasolinaPrecos.db")

# Conectar ao banco, ler a tabela completa e fechar a conexão
conn = sqlite3.connect(db_path)

df = pd.read_sql("SELECT * FROM data", conn)

conn.close()

# Renomear coluna de índice
if 'index_name' in df.columns:
    df = df.rename(columns={'index_name': 'ID'})

# Converter datas
df['DATA INICIAL'] = pd.to_datetime(df['DATA INICIAL'])
df['DATA FINAL'] = pd.to_datetime(df['DATA FINAL'])

# Criar coluna mês/ano
df['DATA INICIAL(Mês/Ano)'] = df['DATA INICIAL'].dt.strftime('%m/%Y')

# Filtrar gasolina comum
df_gasolina_comum = df[df['PRODUTO'] == 'GASOLINA COMUM']

# Exemplos de análises
media_agosto2008 = df_gasolina_comum[df_gasolina_comum['DATA INICIAL(Mês/Ano)'] == '08/2008']['PREÇO MÉDIO REVENDA'].mean()
media_sp_set2007 = df_gasolina_comum[(df_gasolina_comum['DATA INICIAL(Mês/Ano)'] == '09/2007') & (df_gasolina_comum['ESTADO'] == 'SAO PAULO')]['PREÇO MÉDIO REVENDA'].mean()

print(f"Preço médio em Agosto/2008: {media_agosto2008}")
print(f"Preço médio SP Setembro/2007: {media_sp_set2007}")

#Mostrando os data frames
df_gasolina_comum
df
