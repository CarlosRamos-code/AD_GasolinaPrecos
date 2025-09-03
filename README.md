# 📊 Análise de Preços de Gasolina (2000+)

Este projeto realiza a análise de preços da gasolina no Brasil a partir do ano 2000.  
Os dados são integrados a partir de múltiplos arquivos CSV, processados com **Celery + Redis** e armazenados em um banco **SQLite** para posterior análise e filtragem.

---

## 📂 Estrutura do Projeto

- **Dataset**: [Gas Prices in Brazil (Kaggle)](https://www.kaggle.com/datasets/matheusfreitag/gas-prices-in-brazil)  
- **CSV_gasolina_2000+.csv** → Preços da gasolina desde 2000.  
- **CSV_gasolina_2010+.csv** → Preços da gasolina desde 2010.  
- **gasolinaPrecos.db** → Banco de dados **SQLite** que armazena os dados integrados (gerado automaticamente pela task Celery).  
- **sql_celery.py** → Script com a task **Celery** que:
  - Lê os arquivos CSV.  
  - Concatena os datasets.  
  - Salva no banco SQLite (`gasolinaPrecos.db`) em uma tabela chamada `data`.  
  - Faz logging de cada etapa.  
- **FiltrandoDados.py** → Script de análise que:
  - Carrega os CSVs e concatena em um único DataFrame.  
  - Ajusta e converte as colunas de datas.  
  - Cria filtros para **gasolina comum**.  
  - Calcula médias de preços em períodos específicos (ex.: agosto/2008 e setembro/2007 em SP).  
  - Identifica estados com gasolina acima de **R$5**.  
  - Calcula a variação percentual ano a ano para o estado do **Rio de Janeiro**.  
- **docker-compose.yml** → Configuração para subir o serviço **Redis** em container Docker (broker/resultado do Celery).

---

## ⚡ Funcionalidades

- Integração e unificação de múltiplos CSVs com **Celery + Redis**.  
- Persistência em **SQLite** para consultas futuras.  
- Filtros e cálculos estatísticos (preço médio, valores acima de R$5, variações por estado).  
- Automação do pipeline (CSV → SQLite → análise).  
- Logging detalhado para auditoria do processo.  

---

## ▶️ Como Executar
```bash
### 1. Subir o Redis (broker/resultado Celery)
Se tiver Docker:
docker-compose up -d

2. Instalar dependências
pip install pandas celery redis

3. Iniciar o worker Celery na raiz do projeto:
celery -A sql_celery worker -l info

4. Executar a task de carga dos CSVs no Python shell:
from sql_celery import carregar_csv
resultado = carregar_csv.delay()

5. Rodar as análises python em FiltrandoDados.py

````

## 📈 Exemplos de análises implementadas

-Preço médio da gasolina comum em Agosto/2008:

2.736


- Preço médio da gasolina comum em Setembro/2007 em São Paulo:

2.489



- Estados onde a gasolina ultrapassou R$5,00
```bash
             ESTADO          DATA INICIAL(Mês/Ano)    PREÇO MÉDIO REVENDA
12345    RIO DE JANEIRO           03/2021                  5.12
23456    SÃO PAULO                04/2021                  5.05
````



- Variação percentual ano a ano, em relação ao ano anterior(Rio de Janeiro)
```bash
DATA(Ano)    %
2008       4.5%
2009       2.1%
2010       6.8%
...
````

## 🛠️ Tecnologias utilizadas

Python 3.x

- Pandas (manipulação dos dados)

- Celery (orquestração de tarefas assíncronas)

- Redis (mensagens e backend de resultados)

- SQLite (banco de dados leve para persistência)

- Docker (container do Redis)
