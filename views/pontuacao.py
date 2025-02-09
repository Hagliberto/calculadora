import streamlit as st

def exibir_pontuacao():
    st.write(f'✅ :green[**Certos:**] {st.session_state.pontos["Certo"]} ➖ ❌ :red[**Errados:**] {st.session_state.pontos["Errado"]}')
