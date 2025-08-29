
# %%
import sqlite3
import pandas as pd

conn= sqlite3.connect('gasolinaPrecos.db')
# %%
df_2000 = pd.read_csv('gasolina_2000+.csv',sep=',',decimal='.',index_col=0)
df_2010 = pd.read_csv('gasolina_2010+.csv',sep=',',decimal='.',index_col=0)

df_gasolina = pd.concat([df_2000,df_2010])
df.index.name='index_name'
df.to_sql('data',conn, index_label='index_name')
# %%
