import streamlit as st
from openai import OpenAI

st.set_page_config("Privacy Technology Guide", page_icon="🦈")
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

st.header("Privacy Technology Guide")
st.subheader("Policy for Privacy Technology Final Project")
st.text("By: Brigid, Michael, Alison, Brittany")

# Define the decision tree as a nested dictionary
decision_tree = {
    "How will you use your data?": {
        "Answer questions about the data": {
            "How is your data stored?": {
                "Locally": {
                    "Do you want to jointly comput a publically-known function without sharing any raw, noised data?": {
                        "Yes": {"Secure MPC"}, #LEAF
                        "No": {"Do you have a trusted analyst to process the data and a trusted location to store the data centrally?":
                                   {

                                   }}
                    }
                },
                "Centrally": {

                }
            }
        },
        "Send it privately to other parties": {
            "Do you like designing visuals or writing content?": {
                "Designing Visuals": "You might enjoy being a Graphic Designer!",
                "Writing Content": "You might enjoy being a Content Writer!",
            }
        },
        "publically release it": {},
        "train an ML model": {},
        "verify data integrity":{}
    }
}

# Add welcome text
st.write("Welcome to the Privacy Tool! Answer the below questions to understand what privacy tool would be the best fit for your data!")

# Store session state to keep track of progress
if "node" not in st.session_state:
    st.session_state.node = decision_tree
if "history" not in st.session_state:
    st.session_state.history = []

# Function to display the current question or answer
def ask_question(node):
    if isinstance(node, dict):
        question = list(node.keys())[0]
        options = list(node[question].keys())
        choice = st.radio(question, options)

        if st.button("Next"):
            st.session_state.history.append((question, choice))
            st.session_state.node = node[question][choice]
            st.rerun()
    else:
        recommendation_html = """
            <h5>Our Recommendation</h5>
            """
        st.markdown(recommendation_html, unsafe_allow_html=True)
        st.success(node)
        if st.button("Restart"):
            st.session_state.node = decision_tree
            st.session_state.history = []
            st.rerun()

# Display previous choices
if st.session_state.history:
    history_html = """
    <div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>
    <h5>Your Choices So Far:</h5>
    """
    for q, a in st.session_state.history:
        history_html += f"<p><strong>{q}</strong> → <em>{a}</em></p>"
    history_html += "</div>"

    st.markdown(history_html, unsafe_allow_html=True)

# Ask the next question or show the final answer
ask_question(st.session_state.node)
