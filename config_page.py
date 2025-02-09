import streamlit as st
import random

def config_page():
    """Configura a página do Streamlit e adiciona o cabeçalho."""
    st.set_page_config(
        page_title="📢 A.C.T. 2024/2026", 
        page_icon="💰", 
        layout="wide",
        initial_sidebar_state="collapsed"
        )

    # 📌 Criando um contêiner para centralizar o cabeçalho
    with st.container():
        st.markdown(
            """
            <div style="text-align: center; padding: 10px; border-radius: 10px;">
                <h4 style="color: #4A90E2; font-size: 24px;">
                    📜 EXERCÍCIOS DE MATEMÁTICA
                </h4>
            </div>
            """,
            unsafe_allow_html=True
        )
    


# logos.py
def escolher_logo():
    # Lista de URLs dos GIFs ou imagens
    logos = [
        "https://cdn-icons-gif.flaticon.com/10970/10970400.gif",
        "https://gifdb.com/images/high/calendar-mr-sunshine-summer-vksmw63el0cpmck4.gif",
        "https://essencistech.com.br/wp-content/uploads/2018/07/Titkos-tanacsok-noknek-programok-tanfolyamok-napt.gif",
        "https://i.pinimg.com/originals/63/be/5f/63be5f30749ff7be7bb4a633ffac763f.gif",
        "https://cdn.dribbble.com/users/4874/screenshots/1792443/timely_dribbble.gif",
    ]
    
    # Escolher um logo aleatório
    return random.choice(logos)


def rodape():
    """Adiciona o rodapé no final da página."""

    # CSS para o rodapé fixo
    footer_style = """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: var(--background-color);
            color: var(--text-color);
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
            transition: background-color 0.3s ease;
        }
        .footer:hover {
            background-color: #00FF7F;
        }
        
    </style>
    """
    
    # Conteúdo do rodapé
    footer_content = '<div class="footer">👨🏻‍💻 Desenvolvido por <strong>Hagliberto Alves de Oliveira®️</strong></div>'

    # Aplicando o CSS e renderizando o rodapé
    st.markdown(footer_style, unsafe_allow_html=True)
    st.markdown(footer_content, unsafe_allow_html=True)