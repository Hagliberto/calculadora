import streamlit as st
import plotly.express as px
import pandas as pd
import os
from views.pontuacao import exibir_pontuacao

# Diretório onde os históricos diários são armazenados
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# Garante que o diretório exista
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def carregar_historico_por_data(data_escolhida):
    """Carrega o histórico de pontuação incluindo pulos corretamente."""
    data_formatada = data_escolhida.strftime('%d-%m-%Y')
    arquivo_csv = os.path.join(DATA_DIR, f"historico_{data_formatada}.csv")

    if os.path.exists(arquivo_csv):
        df = pd.read_csv(arquivo_csv)
        df["Resultado"] = df["Resultado"].fillna("Pulado")
        return df
    else:
        return pd.DataFrame(columns=['Nome', 'Data', 'Operação', 'Resultado'])

def exibir_historico():
    st.subheader(":blue[**Histórico de Pontuação**]")

    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        exibir_pontuacao()
        data_selecionada = st.date_input("📅 Selecione a data do histórico:", value=pd.to_datetime("today"), format="DD/MM/YYYY")

    with col2:
        with st.expander(f"📜 :blue[**Histórico de Pontuação**] ({data_selecionada.strftime('%d/%m/%Y')})", expanded=False):
            historico_df = carregar_historico_por_data(data_selecionada)
            st.success("Planilha de acertos, erros e pulos")
            
            if historico_df.empty:
                st.warning("Nenhum dado disponível para essa data.")
            else:
                st.data_editor(historico_df, use_container_width=True, hide_index=True)
    
        if not historico_df.empty:
            estatisticas = historico_df.groupby(['Operação'])['Resultado'].value_counts().unstack().fillna(0).reset_index()
            estatisticas["Legenda"] = estatisticas.apply(
                lambda row: f"{row['Operação']} ✅ {row.get('Certo', 0)} | ❌ {row.get('Errado', 0)} | ⏭️ {row.get('Pulado', 0)}", axis=1
            )
            estatisticas_long = estatisticas.melt(id_vars=['Operação', 'Legenda'], var_name='Resultado', value_name='Quantidade')
            estatisticas_long = estatisticas_long[estatisticas_long["Quantidade"] > 0]
    
            if not estatisticas_long.empty:
                fig = px.bar(
                    estatisticas_long,
                    x="Legenda",
                    y="Quantidade",
                    color="Resultado",
                    barmode="stack",
                    title=f"📊 Estatísticas de Acertos, Erros e Pulos ({data_selecionada.strftime('%d/%m/%Y')})",
                    text="Quantidade",
                    color_discrete_map={"Certo": "limegreen", "Errado": "crimson", "Pulado": "dodgerblue"}
                )
                fig.update_traces(textposition="inside")
    
                with st.expander("📈 :blue[**Estatísticas do Dia**]", expanded=False):
                    st.plotly_chart(fig)

    with col3:
        st.image("assets/graph.gif", use_container_width=True, width=100, caption="📊 Gráfico")

def salvar_pontuacao_por_dia(nome, pontos, data, historico):
    """Salva a entrada do histórico incluindo os pulos."""
    
    if not historico:
        return
    
    data_formatada = data.strftime('%d-%m-%Y')
    arquivo_csv = os.path.join(DATA_DIR, f"historico_{data_formatada}.csv")
    df = pd.DataFrame(historico, columns=['Nome', 'Data', 'Operação', 'Resultado'])

    if os.path.exists(arquivo_csv):
        df.to_csv(arquivo_csv, mode='a', header=False, index=False)
    else:
        df.to_csv(arquivo_csv, index=False)

    st.session_state.historico = []
