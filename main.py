import streamlit as st
from openai import OpenAI

st.title("Final Project for Policy in Privacy Technologies")
stuff = st.text_input("What are you looking for in a privacy tool?")
st.write(stuff)
st.checkbox("Public?")
st.selectbox("Choices for Privacy", ["A", "B", "C"])
print(stuff)

def ask_ai(prompt):
    client = OpenAI(
        base_url="https://api.aimlapi.com/v1",
        api_key="f6aefa120b214d27882ca1a172f5fcd8",    
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
with st.spinner("Compiling suggestions..."):
    response = ask_ai("Please recommend some privacy technologies to me, in a short bulleted list")
st.write(response)

