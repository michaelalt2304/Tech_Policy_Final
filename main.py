import streamlit as st

st.title("Final Project for Policy in Privacy Technologies")
stuff = st.text_input("What are you looking for in a privacy tool?")
st.write(stuff)
st.checkbox("Public?")
st.selectbox("Choices for Privacy", ["A", "B", "C"])
print(stuff)