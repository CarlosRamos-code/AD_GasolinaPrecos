# Análise de Preços de Gasolina (2000+)

Este projeto realiza a análise de preços de gasolina no Brasil a partir do ano 2000, integrando dados de múltiplos arquivos CSV em um banco de dados SQLite e aplicando filtros e cálculos específicos para extração de insights.

## Estrutura do Projeto
- **Dataset**: https://www.kaggle.com/datasets/matheusfreitag/gas-prices-in-brazil
- **CSV_gasolina_2000+.csv**: Dados de preços da gasolina a partir do ano 2000.  
- **CSV_gasolina_2010+.csv**: Dados de preços da gasolina a partir do ano 2010.  
- **DB_gasolinaPrecos.db**: Banco de dados SQLite que armazena os dados integrados.  
- **FiltrandoDados.py**: Script Python que:
  - Carrega os CSVs e unifica em um DataFrame.  
  - Ajusta datas e cria filtros para gasolina comum.  
  - Calcula médias de preços em períodos específicos (ex.: agosto/2008 e setembro/2007 em SP).  
  - Identifica estados com preço > R$5.  
  - Calcula variação percentual ano a ano no Rio de Janeiro.  
- **sql.py**: Script Python que:
  - Conecta ao banco `gasolinaPrecos.db`.  
  - Carrega os CSVs, une os dados e insere tudo em uma tabela SQLite chamada `data`.  

## Funcionalidades

- Integração e unificação de múltiplos datasets CSV.  
- Criação de filtros para gasolina comum e períodos específicos.  
- Análise de variações percentuais e identificação de preços elevados por estado.  
- Armazenamento eficiente em SQLite para consultas futuras.  

## Como Usar

```bash
1. Certifique-se de ter Python 3.x instalado.  
2. Instale as dependências necessárias:
   pip install pandas sqlite3
3. Execute os scripts:
   python FiltrandoDados.py
   python sql.py
4. Acesse os dados integrados no banco DB_gasolinaPrecos.db.
