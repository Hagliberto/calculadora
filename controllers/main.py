import streamlit as st
import datetime
import os
import pandas as pd
from models.perguntas import gerar_pergunta
from views.historico import exibir_historico
from views.pontuacao import exibir_pontuacao
from views.historico import salvar_pontuacao_por_dia
from config_page import config_page, escolher_logo, rodape

# Diretório onde os históricos diários serão salvos
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)  # Garante que a pasta de dados exista

def login():
    """Tela de login para capturar o nome do usuário antes de iniciar o jogo."""
    with st.form(key='nome_form'):
        nome = st.text_input('Digite seu nome:')
        confirmar_nome = st.form_submit_button('Confirmar')
        if confirmar_nome and nome:
            st.session_state.nome = nome
            st.toast(f'Bem-vindo(a), {nome}!', icon='🎉')
            st.balloons()
            st.rerun()

def main():
    config_page()
    escolher_logo()
    rodape()
    
    with st.expander("🔢 :blue[**Exercícios de Matemática**]"):
        st.markdown(
            """
            <div style="text-align: center; padding: 15px; border-radius: 8px; background-color: #f0f8ff;">
                <h4 style="color: #4A90E2; font-weight: bold;">
                    🧮 Matemática Básica
                </h4>
                <p style="color: gray; font-size: 15px;">
                    📌 Teste seus conhecimentos resolvendo operações matemáticas de diferentes dificuldades.
                </p>
                <p style="color: gray; font-size: 15px;">
                    📅 Seu progresso será salvo automaticamente para que você possa acompanhar seu desempenho.
                </p>
                <p style="color: gray; font-size: 15px;">
                    📈 Responda corretamente para ganhar pontos e veja seu histórico de acertos, erros e pulos!
                </p>
                <p style="color: #FF5733; font-size: 14px;">
                    ⚠️ Selecione a dificuldade e as operações antes de começar.
                </p>
            </div>
            """,
            unsafe_allow_html=True    
        )

    if 'nome' not in st.session_state:
        login()
        return
    
    st.write(f':green[**Bem vindo(a):**] :blue[**{st.session_state.nome}**]')
    st.subheader(" ", divider="rainbow")

    col1, col2, col3 = st.columns([2, 3, 1])
    
    with col1:
        dificuldade = st.radio("Escolha a dificuldade:", ["Fácil", "Média", "Difícil", "Complexa"], horizontal=True, help="Escolha a dificuldade das operações matemáticas.", key="dificuldade", index=2)
    
    with col2:    
        operacoes = st.multiselect(
            ':blue[**Escolha as operações:**]',
            ['Todas', 'Adição', 'Subtração', 'Multiplicação', 'Divisão', 'Exponenciação'],
            placeholder="Selecione pelo menos uma operação", 
            help="Escolha as operações matemáticas que deseja praticar.", 
            key="operacoes",
            default=["Todas"]
        )
        
    with col3:
        mostrar_historico = st.toggle('Mostrar histórico', help="Clique para exibir o histórico de pontuação do dia.")

    if not operacoes:
        st.error("Por favor, selecione pelo menos uma operação para continuar.")
        return

    operacoes_mapeadas = {
        'Adição': '+',
        'Subtração': '-',
        'Multiplicação': '*',
        'Divisão': '/',
        'Exponenciação': '**'
    }
    
    operacoes_selecionadas = [operacoes_mapeadas[op] for op in operacoes if op in operacoes_mapeadas] if 'Todas' not in operacoes else list(operacoes_mapeadas.values())

    if 'pontos' not in st.session_state:
        st.session_state.pontos = {'Certo': 0, 'Errado': 0, 'Pulado': 0}

    if 'pergunta' not in st.session_state or 'resposta_correta' not in st.session_state:
        st.session_state.pergunta, st.session_state.resposta_correta, st.session_state.operacao = gerar_pergunta(operacoes_selecionadas, dificuldade.lower())
    if 'historico' not in st.session_state:
        st.session_state.historico = []
    if 'inicio' not in st.session_state:
        st.session_state.inicio = datetime.datetime.now().strftime('%d-%m-%Y')

    if mostrar_historico:
        exibir_historico()
    else:
        st.subheader(":blue[**Perguntas**]")
        with st.form(key='resposta_form'):
            st.write(f':blue[**Exercício**] :gray[**({st.session_state.operacao}):**] :red[**{st.session_state.pergunta}**]')
            col1, col2, col3 = st.columns([1,3,1])
            
            with col2:
                if "campo_resposta" not in st.session_state:
                    st.session_state["campo_resposta"] = ""
    
                resposta_usuario = st.text_input(":green[**Digite sua resposta⤵️**]", key="campo_resposta", placeholder="Insira sua resposta aqui")
                st.caption("Digite sua resposta e clique em 'Responder' para verificar se está correta.")
                # exibir_pontuacao()


            with col2:
                col4, col5 = st.columns(2) 
                with col4:               
                    responder = st.form_submit_button(":green[**Responder**] :blue[**Pergunta**]", help="Digite sua resposta e clique em 'Responder' para verificar se está correta.", icon=":material/add_task:")
                with col5:    
                    pular = st.form_submit_button(":green[**Pular**] :blue[**Pergunta**]", help="Pula a pergunta atual e exibe uma nova pergunta", icon=":material/move_down:")

            if responder:
                try:
                    resposta_usuario = float(resposta_usuario.strip()) if resposta_usuario.strip() else None

                    if resposta_usuario is not None:
                        resultado = "Certo" if resposta_usuario == st.session_state.resposta_correta else "Errado"
                        st.session_state.pontos[resultado] += 1

                        data_atual = datetime.datetime.now().date()
                        ultima_resposta = [[st.session_state.nome, data_atual, st.session_state.operacao, resultado]]
                        salvar_pontuacao_por_dia(st.session_state.nome, st.session_state.pontos, data_atual, ultima_resposta)

                        st.session_state.pop("campo_resposta", None)

                        st.session_state.pergunta, st.session_state.resposta_correta, st.session_state.operacao = gerar_pergunta(operacoes_selecionadas, dificuldade.lower())

                        st.rerun()
                    else:
                        st.error("Por favor, insira um número válido.")
                except ValueError:
                    st.error("Por favor, insira um número válido.")

            if pular:
                st.session_state.pontos["Pulado"] += 1

                data_atual = datetime.datetime.now().date()
                st.session_state.historico.append([st.session_state.nome, data_atual, st.session_state.operacao, "Pulado"])

                st.session_state.pergunta, st.session_state.resposta_correta, st.session_state.operacao = gerar_pergunta(operacoes_selecionadas, dificuldade.lower())

                salvar_pontuacao_por_dia(st.session_state.nome, st.session_state.pontos, data_atual, st.session_state.historico)

                st.rerun()

    st.subheader(" ", divider="rainbow")
    exibir_pontuacao()
