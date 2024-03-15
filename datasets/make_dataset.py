import pathlib
import os
import sys
import boto3

CURRENT_DIR = pathlib.Path(__file__).resolve().parent.parent

# Adicione o diretório ao sys.path
sys.path.append(str(CURRENT_DIR))

from config import config

import pandas as pd
from datetime import datetime
import yfinance as yf

# data parameters
start_date = datetime(2022,1,1)
end_date = datetime(2024,1,1)

# getting the data
df_raw = yf.download('AAPL', start=start_date, end=end_date)
df_raw.reset_index(inplace=True)




# Transform Data

## Drop Columns
# Data: A coluna "Date" geralmente não é usada como uma feature nos modelos de previsão financeira, pois a ordem temporal já é capturada pela sequência das linhas do dataframe.

# Adj Close: A coluna "Adj Close" representa o preço de fechamento ajustado de uma ação, levando em consideração eventos como dividendos, divisões de ações, etc. Não vamos utilizar o preço de fechamento ajustado para a análise específica. Iremos descartar essa coluna para reduzir a dimensionalidade dos dados ou simplificar a análise.

df_transform = df_raw.copy()
df_transform.drop(columns=['Date'], inplace=True)
df_transform.drop(columns=['Adj Close'], inplace=True)




# A estratégia abaixo cria um conjunto de dados onde cada linha contém um conjunto de features e um target (o valor da primeira coluna no dia seguinte). Como o problema proposto é previsão de séries temporais, usamos dados históricos para prever o próximo valor em uma série temporal. Neste caso, estamos utilizando a abertura do dia seguinte como target do dia anterior.

## Prepare Dataset
# Todas as linhas, exceto a última.
features = df_transform.iloc[:-1, :]

# Todas as linhas, exceto a primeira.
# Dessa forma, conseguimos pegar o fechamento desse dia.
targets = df_transform.iloc[1:, 0]

# Adiciona os targets como uma nova coluna em features, na primeira posição.
features.insert(0, 'Target', targets.values)

df_final = features.copy()
df_final = df_final.sample(frac=1, random_state=config.SEED)




## Split Data
# Número de linhas para treinamento (80%)
train_size = int(len(df_final) * 0.8)

# DataFrame de treinamento
train_data = df_final.iloc[:train_size]

# DataFrame de teste
test_data = df_final.iloc[train_size:]

print('Train shape', len(train_data))
print('Test shape', len(test_data))



# Load to S3 Bucket
train_data.to_csv(config.TRAIN_CSV_PATH, index=False, header=False)
test_data.to_csv(config.TEST_CSV_PATH, index=False, header=False)