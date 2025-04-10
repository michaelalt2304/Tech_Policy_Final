import streamlit as st
from openai import OpenAI

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

st.header("Privacy in Policy Technology Final Project")
st.subheader("By: Brigid, Michael, Alison, Brittany")

def make_slider(label):
    return st.slider(label, min_value = 1, max_value = 5, value = 3, step = 1)
with st.form("personalization"):
    use_case = st.selectbox("Which best applies to your use case?", \
                ["I am conducting analysis on data (locally or centrally)", \
                    "I need to send data to someone else", \
                    "I need another party to analyze data but not see raw data", \
                    "I want to publish data to the public", \
                    "I want to publish analysis results to the public", \
                    "I want to audit or verify system/data integrity", \
                    "I want my system to be verifiable/trusted by another party"],
                    index = None,
                    placeholder = "Please select one...")
    direct_PII = st.checkbox("My data contains direct PII")
    sparse = st.checkbox("My data is highly unique/sparse")
    noise = st.checkbox("I can add noise to data")
    synth = st.checkbox("My data can be represented synthetically")
    raw = st.checkbox("Data can be seen raw")
    st.write("How much do each of the following characteristics apply to your data?")
    adversaries = make_slider("I fear adversaries gaining access to the data")
    linked = make_slider("This data could be linked to other accessible sets")
    recons = make_slider("The data could be reconstructed")
    trust = make_slider("There is a trusted third party that can handle the data")
    curious = make_slider("I can assume honest-but-curious parties")
    malicious = make_slider("I assume malicious parties")
    privacy = make_slider("I value privacy even at the cost of accuracy")
    reversible = make_slider("I want noise that can be irreversibly applied to data")
    verifiable = make_slider("The system needs to be independently verifiable")
    other = st.text_area("Anything else you would like to specify? Please note, we cannot necessarily guarantee the security of this platform, so please omit any proprietary data")

    submitted = st.form_submit_button("Generate advice!")



if submitted:
    with st.spinner("Compiling suggestions..."):
        response = ask_ai("Please recommend some privacy technologies to me, in a short bulleted list")
    st.write(response)

