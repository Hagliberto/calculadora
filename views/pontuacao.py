import streamlit as st
import pandas as pd
from models.pontuacao import salvar_usuario, carregar_usuarios, excluir_usuario, atualizar_usuario

def exibir_pontuacao():
    st.write(f'✅ :green[**Certos:**] {st.session_state.pontos["Certo"]} ➖ ❌ :red[**Errados:**] {st.session_state.pontos["Errado"]} ➖ ⏭️ :blue[**Pulados:**] {st.session_state.pontos["Pulado"]}')

def gerenciar_usuarios():
    st.title("Gerenciamento de Usuários")
    
    # Exibir usuários cadastrados
    st.subheader("Usuários Cadastrados")
    usuarios_df = carregar_usuarios()
    st.dataframe(usuarios_df)
    
    # Formulário para adicionar um novo usuário
    st.subheader("Adicionar Usuário")
    nome = st.text_input("Nome do usuário")
    pontuacao = st.number_input("Pontuação inicial", min_value=0, step=1)
    if st.button("Salvar Usuário"):
        if nome:
            salvar_usuario(nome, pontuacao)
            st.success(f"Usuário {nome} salvo com sucesso!")
            st.rerun()
        else:
            st.warning("O nome não pode estar vazio.")
    
    # Formulário para excluir um usuário
    st.subheader("Excluir Usuário")
    usuario_id_excluir = st.number_input("ID do usuário a excluir", min_value=1, step=1)
    if st.button("Excluir Usuário"):
        excluir_usuario(usuario_id_excluir)
        st.success("Usuário excluído com sucesso!")
        st.rerun()
    
    # Formulário para atualizar um usuário
    st.subheader("Atualizar Usuário")
    usuario_id_atualizar = st.number_input("ID do usuário a atualizar", min_value=1, step=1)
    novo_nome = st.text_input("Novo Nome")
    nova_pontuacao = st.number_input("Nova Pontuação", min_value=0, step=1)
    if st.button("Atualizar Usuário"):
        atualizar_usuario(usuario_id_atualizar, novo_nome if novo_nome else None, nova_pontuacao if nova_pontuacao else None)
        st.success("Usuário atualizado com sucesso!")
        st.rerun()

# Se quiser chamar essa função em sua aplicação principal
if __name__ == "__main__":
    gerenciar_usuarios()