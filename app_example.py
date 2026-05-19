import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 

# comentários básicos do Streamlit

st.title("Aula 06 - Streamlit")
st.write("Olá, seja bem-vindo à aula 06 de Streamlit!")

st.header("Este é um header")
st.subheader("Este é um subheader") 
st.text("Este é um texto simples")
st.markdown("Este é um texto em **negrito** e em *itálico*")

# exibindo um DataFrame

data = { 
    "Nome": ["Alice", "Bob", "Charlie"],
    "Idade": [25, 30, 35],
    "Salário": [50000, 60000, 70000]    
}

df = pd.DataFrame(data)
st.dataframe(df)
st.table(df)

# usando gráficos

fig, ax = plt.subplots()
ax.bar(df["Nome"], df["Salário"])
st.pyplot(fig)

if st.button("Clique aqui"):
    st.write("Você clicou no botão!")

idade = st.slider("Selecione a idade", 0, 100, 25)
st.write(f"A idade selecionada é: {idade}")

opcao = st.selectbox(
    "Selecione uma opção", 
    ["Opção 1", "Opção 2", "Opção 3"]
)

st.write(f"Departamento selecionado: {opcao}")

