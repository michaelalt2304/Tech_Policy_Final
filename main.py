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
    reversible = make_slider("I want noise that can be reversibly applied to data")
    verifiable = make_slider("The system needs to be independently verifiable")
    other = st.text_area("Anything else you would like to specify? Please note, we cannot necessarily guarantee the security of this platform, so please omit any proprietary data")

    submitted = st.form_submit_button("Generate advice!")



if submitted:
    with st.spinner("Compiling suggestions..."):
        prompt = "Please recommend some privacy technologies to me, in a short bulleted list with descriptions, with the following conditions: " + \
                    "Center the discussion around "
        prompt += "Use Synthetic Data, or Private GANs. Avoid k-anonymity/l-diversity unless heavily aggregated" if use_case == "I want to publish analysis results to the public" and (privacy == 5 or linked == False or not direct_PII) else \
                    "Differential Privacy (Central DP) for aggregated results. If no trust: use Local DP" if (trust >= 3 or curious >= 3) and use_case == "I want to publish analysis results to the public" else \
                    "Local DP" if trust <= 2 else \
                    "Use Public Key Cryptography for encryption. Optionally add Attestation for system-level trust" if use_case == "I need to send data to someone else" and direct_PII else \
                    "Use Homomorphic Encryption" if use_case == "I need another party to analyze data but not see raw data" and trust else \
                    "Use Multi Party Encryption" if (use_case == "I need another party to analyze data but not see raw data" and  trust <= 2 and malicious <= 2) else \
                    "Consider Trusted Execution Environment (TEE) for hardware-level protection" if use_case == "I am conducting analysis on data (locally or centrally)" and noise == False else \
                    "Use Multi Party Encryption with redundancy and crypto" if use_case == "I want to publish analysis results to the public" and malicious > 3 else \
                    "Use Local Differential Privacy. Good for collecting noisy aggregates. Add privacy budget management if long-term use" if noise == True and use_case == "I need another party to analyze data but not see raw data" or use_case == "I am conducting analysis on data (locally or centrally)" else \
                    "Use Attestation, TEE, and Cryptographic Hashes. Use Blockchain if decentralized auditable log is needed" if use_case == "I want to audit or verify system/data integrity" else \
                    "Use Synthetic Data" if privacy <= 2 and synth else \
                    "Use Blockchain" if reversible >= 3 and use_case == "I want to audit or verify system/data integrity" else \
                    "Use Blockchain. Especially for distributed audit trails. GDPR/erasure caveats apply" if reversible >= 2 and use_case == "I want my system to be verifiable/trusted by another party" else \
                    "Use Federated Learning, combine with Secure Aggregation, DP, or MPC to reinforce privacy depending on the threat model." if use_case == "I am conducting analysis on data (locally or centrally)" and malicious >= 3 and trust <= 2 else \
                    use_case if use_case else "Privacy for the below characteristics"
        prompt += ". Also factor in for our use case that we "
        prompt += "do " if direct_PII else "do not " 
        prompt += "have direct PII, "
        prompt += "do " if sparse else "do not "
        prompt += "have sparse data, "
        prompt += "can " if noise else "cannot "
        prompt += "add noise to the data, "
        prompt += "can " if synth else "cannot " 
        prompt += "add synthetic data, and " 
        prompt += "can " if raw else "cannot " 
        prompt += " expose the raw data. " 
        prompt += "Also account for the following attributes, if any: " 
        prompt += "\nI fear adversaries gaining access to the data" if adversaries > 3 else ""
        prompt += "\nThe data could be linked to other data sets" if linked > 3 else "" 
        prompt += "\nThe data could be reconstructed" if recons > 3 else ""
        prompt += "\nThere is a trusted third party that can handle the data" if trust > 3 else ""
        prompt += "\nI assume malicious parties" if malicious > 3 else ""
        prompt += "\nI value privacy even at the cost of accuracy" if privacy > 3 else ""
        prompt += "\nI want noise that can be reversibly applied to data" if reversible > 3 else ""
        prompt += "\nThe system needs to be independently verifiable" if verifiable > 3 else ""
        prompt += "."
        prompt += f" Additionally, consider {other}." if other else "" 
        
                    
                    
        response = ask_ai(prompt)
    st.write(response)

