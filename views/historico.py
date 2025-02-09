import streamlit as st
import plotly.express as px
import pandas as pd
import os

# Diretório onde os históricos diários são armazenados
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

def carregar_historico_por_data(data_escolhida):
    """Carrega o histórico de pontuação de um arquivo específico baseado na data escolhida."""
    data_formatada = data_escolhida.strftime('%Y-%m-%d')
    arquivo_csv = os.path.join(DATA_DIR, f"historico_{data_formatada}.csv")

    if os.path.exists(arquivo_csv):
        return pd.read_csv(arquivo_csv)
    else:
        return pd.DataFrame(columns=['Nome', 'Data', 'Operação', 'Resultado'])

def exibir_historico():
    st.title(":blue[**Histórico de Pontuação**]")

    # Seletor de data para escolher o histórico de um dia específico
    data_selecionada = st.date_input("📅 Selecione a data do histórico:", value=pd.to_datetime("today"), format="DD/MM/YYYY")

    with st.expander(f"📜 :blue[**Histórico de Pontuação**] ({data_selecionada.strftime('%d/%m/%Y')})", expanded=False):
        historico_df = carregar_historico_por_data(data_selecionada)
        st.success("Planilha de acertos e erros")
        st.data_editor(historico_df, use_container_width=True)

    if not historico_df.empty:
        estatisticas = historico_df.groupby(['Operação'])['Resultado'].value_counts().unstack().fillna(0).reset_index()

        # Criar uma legenda personalizada com estatísticas
        estatisticas["Legenda"] = estatisticas.apply(
            lambda row: f"{row['Operação']} ✅ {row.get('Certo', 0)} | ❌ {row.get('Errado', 0)}", axis=1
        )

        # Transformar para formato longo para exibição no gráfico
        estatisticas_long = estatisticas.melt(id_vars=['Operação', 'Legenda'], var_name='Resultado', value_name='Quantidade')

        fig = px.bar(
            estatisticas_long,
            x="Legenda",
            y="Quantidade",
            color="Resultado",
            barmode="stack",
            title=f"📊 Estatísticas de Acertos e Erros ({data_selecionada.strftime('%d/%m/%Y')})",
            text="Quantidade",
            color_discrete_map={"Certo": "limegreen", "Errado": "crimson"}
        )
        fig.update_traces(textposition="inside")

        with st.expander("📈 :blue[**Estatísticas do Dia**]", expanded=False):
            st.plotly_chart(fig)
