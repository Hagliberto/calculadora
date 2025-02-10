import streamlit as st
import datetime
import os
import pandas as pd
from models.perguntas import gerar_pergunta
from views.historico import exibir_historico
from views.pontuacao import exibir_pontuacao
from views.historico import salvar_pontuacao_por_dia
from config_page import config_page, rodape, render_logo
import random
import time  # Importe o módulo time corretamente

# Diretório onde os históricos diários serão salvos
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)  # Garante que a pasta de dados exista

def login():
    """Tela de login para capturar o nome do usuário antes de iniciar o jogo."""
    col1, col2, col3 = st.columns([1, 5, 1])
    with col1:
        st.image("assets/cat-cats.gif", use_container_width=True, caption=" ")
    with col2:
        with st.form(key='nome_form'):
            nome = st.text_input('Digite seu nome:')
            confirmar_nome = st.form_submit_button('Confirmar')
            if confirmar_nome and nome:
                st.session_state.nome = nome
                st.toast(f'Bem-vindo(a), {nome}!', icon='🎉')
                st.balloons()
                st.rerun()

    with col3:
        st.image("assets/study-cat.gif", use_container_width=True, caption=" ")

    st.subheader(" ", divider="rainbow")

def main():
    config_page()
    render_logo()

    # Verificação do PIN
    if 'pin_validated' not in st.session_state:
        st.session_state.pin_validated = False
    if 'show_pin' not in st.session_state:
        st.session_state.show_pin = False

    if not st.session_state.pin_validated:
        st.markdown(
            """
            <style>
            .title {text-align: center; color: #444; font-size: 28px;}
            .pin-input {width: 100%; text-align: center; font-size: 20px; padding: 10px;
                        border-radius: 8px; border: 1px solid #ccc; transition: 0.3s;}
            .pin-input:focus {border-color: #007BFF; outline: none;}
            .button-style {background-color: #007BFF; color: white; border: none;
                           padding: 10px 20px; border-radius: 8px; font-size: 16px;
                           transition: 0.3s; width: 100%;}
            .button-style:hover {background-color: #0056b3;}
            </style>
            """,
            unsafe_allow_html=True
        )

        st.sidebar.markdown('<h2 class="title">🔒 Acesso Restrito</h2>', unsafe_allow_html=True)

        # Adicionando a imagem no topo
        # Lista de URLs das imagens
        image_urls = [
            "https://static.wikia.nocookie.net/tkoc/images/c/c8/Eternal_Sailor_Moon.png",
            "https://cinevibes.com.br/wp-content/uploads/2024/07/sailor-moon-with-friends-416crfd863r99xxm.jpg",
            "https://oldflix-images-cdn.b-cdn.net/images/cover/5d9dd3ba437c361034ed0c2f.jpg",
            "https://static.wikia.nocookie.net/listofdeaths/images/4/48/Sailor_Moon_Crystal_poster.jpg",
            "https://i.pinimg.com/564x/51/62/0f/51620fee995360cb9f1b7aa373b40ad9.jpg",
            "https://i.pinimg.com/originals/9d/3b/3f/9d3b3f2d9d6c4d7d5b2c6c4f3e7f0d8d.jpg",
            "https://i.pinimg.com/originals/9d/3b/3f/9d3b3f2d9d6c4d7d5b2c6c4f3e7f0d8d.jpg",
            "https://i.pinimg.com/originals/9d/3b/3f/9d3b3f2d9d6c4d7d5b2c6c4f3e7f0d8d.jpg",
            "https://i.pinimg.com/originals/9d/3b/3f/9d3b3f2d9d6c4d7d5b2c6c4f3e7f0d8d.jpg",
            
            
        ]

        # Inicializa o estado da imagem para alternar a cada acesso
        if 'current_image' not in st.session_state:
            st.session_state.current_image = random.choice(image_urls)

        # Exibição da imagem de forma aleatória a cada acesso
        st.image(
            st.session_state.current_image,
            caption="Bem-vindo ao Sistema",
            use_container_width=True
        )

        # Título centralizado
        st.markdown(
            """
            <style>
            .title {text-align: center; color: #444; font-size: 28px; margin-top: 10px;}
            </style>
            """,
            unsafe_allow_html=True
        )

        # Verificação de PIN usando st.form
        with st.sidebar.form(key="pin_form", clear_on_submit=False):
            col1, col2 = st.columns([1.1, 0.9])

            with col1:
                pin_type = "password" if not st.session_state.show_pin else "default"
                pin = st.text_input(
                    "Digite o PIN para acessar:",
                    type=pin_type,
                    placeholder="💝",
                    label_visibility="collapsed"
                )

            with col2:
                # Botão de validação dentro do formulário
                submit = st.form_submit_button("🔑 Validar", type="primary", help="Pessoas importantes para você")

                # Validação do PIN
                valid_pins = ["Hagliberto", "Cláudia", "Shuelym"]
                normalized_valid_pins = {p.lower() for p in valid_pins}

            if submit:
                with st.spinner("Validando PIN..."):
                    time.sleep(2)  # Use o módulo time corretamente
                    if pin.lower() in normalized_valid_pins:
                        st.toast("PIN correto! Acesso liberado.", icon="🎉")
                        st.session_state.pin_validated = True
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    elif pin:
                        st.toast("PIN incorreto. Tente novamente.", icon="⚠️")

        # Retorna para evitar que o restante do código seja executado
        return

    rodape()

    with st.sidebar.expander("🔢 :blue[**Exercícios de Matemática**]"):
        st.markdown(
            """
            <div style="text-align: center; padding: 15px; border-radius: 8px; background-color: #05fad5;">
                <h4 style="color: black; font-weight: bold;">
                    🧮 Matemática Básica
                </h4>
                <p style="color: black; font-size: 15px;">
                    📌 Teste seus conhecimentos resolvendo operações matemáticas de diferentes dificuldades.
                </p>
                <p style="color: black; font-size: 15px;">
                    📅 Seu progresso será salvo automaticamente para que você possa acompanhar seu desempenho.
                </p>
                <p style="color: black; font-size: 15px;">
                    📈 Responda corretamente para ganhar pontos e veja seu histórico de acertos, erros e pulos!
                </p>
                <p style="color: red; font-size: 14px;">
                    ⚠️ Selecione a dificuldade e as operações antes de começar.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Inicialização do nome se não estiver no session_state
    if 'nome' not in st.session_state:
        st.session_state.nome = ""

    if not st.session_state.nome and st.session_state.pin_validated:
        login()
        return

    st.sidebar.write(f':blue[**Bem vindo(a):**] :green[**{st.session_state.nome}**]')
    st.sidebar.subheader(" ", divider="rainbow")

    col1, col2, col3 = st.columns([2, 3, 1])

    with col1:
        dificuldade = st.sidebar.radio(f":blue[**Escolha a dificuldade:**]", ["Fácil", "Média", "Difícil", "Complexa"], horizontal=True, help="Escolha a dificuldade das operações matemáticas.", key="dificuldade", index=2)
    st.sidebar.subheader(" ", divider="rainbow")
    with col2:
        operacoes = st.sidebar.multiselect(
            ':blue[**Escolha as operações:**]',
            ['Todas', 'Adição', 'Subtração', 'Multiplicação', 'Divisão', 'Exponenciação'],
            placeholder="Selecione pelo menos uma operação",
            help="Escolha as operações matemáticas que deseja praticar.",
            key="operacoes",
            default=["Todas"]
        )
    st.sidebar.subheader(" ", divider="rainbow")
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

        exibir_pontuacao()
        with st.form(key='resposta_form'):

            col1, col2, col3 = st.columns([1,3,1])

            with col1:
                st.success(f':blue[**Exercício**] :gray[**({st.session_state.operacao})**]')
                st.warning(f':red[**{st.session_state.pergunta}**]')

            with col2:
                if "campo_resposta" not in st.session_state:
                    st.session_state["campo_resposta"] = ""

                resposta_usuario = st.text_input(":green[**Digite sua resposta⤵️**]", key="campo_resposta", placeholder="✍🏻 Insira sua resposta aqui", help="Evite pular 🦘 perguntas")

                # Converter vírgula para ponto e transformar em número
                try:
                    resposta_numerica = float(resposta_usuario.replace(',', '.'))
                except ValueError:
                    resposta_numerica = None

                # st.caption("Digite sua resposta e clique em 'Responder' para verificar se está correta.")
                # exibir_pontuacao()

            with col2:
                col4, col5 = st.columns(2)
                with col4:
                    responder = st.form_submit_button(":green[**Responder**] **Pergunta**", help="Digite sua resposta e clique em 'Responder' para verificar se está correta.", icon=":material/add_task:")
                with col5:
                    pular = st.form_submit_button(":green[**Pular**] **Pergunta**", help="Pula a pergunta atual e exibe uma nova pergunta", icon=":material/move_down:")

            with col3:
                st.image("assets/cat-cats.gif", use_container_width=True, width=100, caption=" ")

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
                        with col2:
                            st.error("Por favor, insira um número válido.")
                            st.toast("Por favor, insira um número válido.", icon=":material/pin:")
                except ValueError:
                    with col2:
                        st.error("Por favor, insira um número válido.")
                        st.toast("Por favor, insira um número válido.", icon=":material/123:")

            if pular:
                st.session_state.pontos["Pulado"] += 1

                data_atual = datetime.datetime.now().date()
                st.session_state.historico.append([st.session_state.nome, data_atual, st.session_state.operacao, "Pulado"])

                st.session_state.pergunta, st.session_state.resposta_correta, st.session_state.operacao = gerar_pergunta(operacoes_selecionadas, dificuldade.lower())

                salvar_pontuacao_por_dia(st.session_state.nome, st.session_state.pontos, data_atual, st.session_state.historico)

                st.rerun()

    st.subheader(" ", divider="rainbow")
    exibir_pontuacao()
