import pandas as pd
import os

# Caminho correto para a pasta `data/`, independentemente de onde o script for executado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório do próprio arquivo
DATA_DIR = os.path.join(BASE_DIR, "..", "data")  # Caminho correto para a pasta `data`
USERS_CSV = os.path.join(DATA_DIR, "usuarios.csv")
SCORES_CSV = os.path.join(DATA_DIR, "historico_pontuacao.csv")

# Garante que a pasta `data/` exista antes de tentar salvar qualquer coisa
os.makedirs(DATA_DIR, exist_ok=True)

# Se os arquivos não existirem, cria CSVs com cabeçalhos corretos
if not os.path.exists(USERS_CSV):
    pd.DataFrame(columns=['ID', 'Nome', 'Pontuacao']).to_csv(USERS_CSV, index=False)

if not os.path.exists(SCORES_CSV):
    pd.DataFrame(columns=['Nome', 'Hora de Início', 'Operação', 'Resultado']).to_csv(SCORES_CSV, index=False)

def salvar_usuario(nome, pontuacao):
    df = pd.read_csv(USERS_CSV)
    novo_id = df['ID'].max() + 1 if not df.empty else 1
    novo_usuario = pd.DataFrame([[novo_id, nome, pontuacao]], columns=['ID', 'Nome', 'Pontuacao'])
    df = pd.concat([df, novo_usuario], ignore_index=True)
    df.to_csv(USERS_CSV, index=False)

def carregar_usuarios():
    return pd.read_csv(USERS_CSV)

def listar_usuarios():
    df = carregar_usuarios()
    return df[['ID', 'Nome']]

def excluir_usuario(usuario_id):
    df = carregar_usuarios()
    df = df[df['ID'] != usuario_id]
    df.to_csv(USERS_CSV, index=False)

def atualizar_usuario(usuario_id, novo_nome=None, nova_pontuacao=None):
    df = carregar_usuarios()
    if usuario_id in df['ID'].values:
        if novo_nome:
            df.loc[df['ID'] == usuario_id, 'Nome'] = novo_nome
        if nova_pontuacao is not None:
            df.loc[df['ID'] == usuario_id, 'Pontuacao'] = nova_pontuacao
        df.to_csv(USERS_CSV, index=False)

def salvar_pontuacao(nome, pontos, inicio, historico):
    df = pd.DataFrame(historico, columns=['Nome', 'Hora de Início', 'Operação', 'Resultado'])
    try:
        historico_df = pd.read_csv(SCORES_CSV)
        historico_df = pd.concat([historico_df, df], ignore_index=True)
    except FileNotFoundError:
        historico_df = df
    historico_df.to_csv(SCORES_CSV, index=False)

def carregar_pontuacoes():
    try:
        df = pd.read_csv(SCORES_CSV)
        df['Hora de Início'] = pd.to_datetime(df['Hora de Início']).dt.strftime('%d/%m/%Y')
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['Nome', 'Hora de Início', 'Operação', 'Resultado'])
