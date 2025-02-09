import pandas as pd
import os

# Caminho correto para a pasta `data/`, independentemente de onde o script for executado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório do próprio arquivo
DATA_DIR = os.path.join(BASE_DIR, "..", "data")  # Caminho correto para a pasta `data`
CSV_FILE = os.path.join(DATA_DIR, "historico_pontuacao.csv")

# Garante que a pasta `data/` exista antes de tentar salvar qualquer coisa
os.makedirs(DATA_DIR, exist_ok=True)

# Se o arquivo não existir, cria um CSV com os cabeçalhos corretos
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=['Nome', 'Hora de Início', 'Operação', 'Resultado']).to_csv(CSV_FILE, index=False)

def salvar_pontuacao(nome, pontos, inicio, historico):
    df = pd.DataFrame(historico, columns=['Nome', 'Hora de Início', 'Operação', 'Resultado'])
    try:
        historico_df = pd.read_csv(CSV_FILE)
        historico_df = pd.concat([historico_df, df], ignore_index=True)
    except FileNotFoundError:
        historico_df = df
    historico_df.to_csv(CSV_FILE, index=False)

def carregar_pontuacoes():
    try:
        df = pd.read_csv(CSV_FILE)
        df['Hora de Início'] = pd.to_datetime(df['Hora de Início']).dt.strftime('%d/%m/%Y')
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['Nome', 'Hora de Início', 'Operação', 'Resultado'])
