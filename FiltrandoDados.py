
#%%
import pandas as pd


# Carregando o conjunto de dados, combinando em um único dataframe e Renomeando a coluna de ID
df_2000 = pd.read_csv('gasolina_2000+.csv',sep=',',decimal='.')
df_2010 = pd.read_csv('gasolina_2010+.csv',sep=',',decimal='.')

df_gasolina = pd.concat([df_2000,df_2010])
df = df_gasolina.rename(columns={'Unnamed: 0': 'ID'})

#Verificando as informações do meu DataFrame
df.info()

# Selecionando as colunas DATA INICIAL e DATA FINAL e Convertendo a formatação para DateTime

df['DATA INICIAL'] = pd.to_datetime(df['DATA INICIAL'])
df['DATA FINAL'] = pd.to_datetime(df['DATA INICIAL'])

#Criando uma Coluna para Representar o mês/ Ano para melhor filtragem
df['DATA INICIAL(Mês/Ano)'] = df['DATA INICIAL'].apply(lambda x:'{:-02d}'.format(x.month)) + '/'  + df['DATA INICIAL'].apply(lambda x:'{}'.format(x.year)) 

#Listando os tipos de produtos contidos na base de Dados 
df['PRODUTO'].value_counts()

#Filtrando Dados para gasolina Comum
df_filtro = df ['PRODUTO'] == 'GASOLINA COMUM'
df2 = df[df_filtro]

#Preço médio da gasolina em Agosto de 2008
df_media_Agosto2008 = df2[df2['DATA INICIAL(Mês/Ano)'] == '08/2008']['PREÇO MÉDIO REVENDA'].mean()

#Preço médio da gasolina em Setembro/2007 no estado de São Paulo
df_media_SP_Setembro2007 = df2[(df2['DATA INICIAL(Mês/Ano)'] == '09/2007') & (df2['ESTADO'] == 'SAO PAULO')]['PREÇO MÉDIO REVENDA'].mean()

#Estados em que a gasolina está mais cara que 5 reais na amostragem
df_estados_PrecoGasolina_MaiorQue5 = df2[df2['PREÇO MÉDIO REVENDA'] > 5] [['ESTADO','DATA INICIAL(Mês/Ano)','PREÇO MÉDIO REVENDA']]

# %%
#Criando uma tabela que contenha a variação percentual ano a ano para o estado do Rio de janeiro

df2['MES']= df2['DATA FINAL'].apply(lambda x: x.month)
df_rio = df2[df2['ESTADO'] == 'RIO DE JANEIRO']

df_mes_rio = df_rio.groupby('DATA INICIAL(Mês/Ano)')[['PREÇO MÉDIO REVENDA', 'MES']].last()

(df_mes_rio[df_mes_rio['MES'] == 12] / df_mes_rio[df_mes_rio['MES'] == 12].shift(1) -1) * 100

# %%
