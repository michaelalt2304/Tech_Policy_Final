import streamlit as st
from openai import OpenAI
from streamlit import slider

from decision_tree import decision_tree, legal_decision_tree, privacy_budget_decision_tree

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

st.header("Privacy Tool")
st.subheader("Policy for Privacy Technology Final Project")
st.text("By: Brigid, Michael, Alison, Brittany")

# --- INITIALIZE APP STATE ---
if "node" not in st.session_state:
    st.session_state.node = decision_tree
if "history" not in st.session_state:
    st.session_state.history = []
if "stage" not in st.session_state:
    st.session_state.stage = "main"
if "final_recommendation" not in st.session_state:
    st.session_state.final_recommendation = ""
if "show_first_recommendation" not in st.session_state:
    st.session_state.show_first_recommendation = False
if "slider_submitted" not in st.session_state:
    st.session_state.slider_submitted = False
if "summarize_recommendations" not in st.session_state:
    st.session_state.summarize_recommendations = False

# -- SLIDER RECOMMENDATION

def get_slider_text(slider_value):
    if slider_value > 6:
        return "To prioritize strong privacy guarantees over data accuracy, use a small epsilon (<1) and use a very small value (<10^{-7}) or 0 for delta. Expect high noise and impacts to analytical utility. Selecting these parameters requires great care. Work with a privacy expert to ensure the value of these parameters works well with your data."
    elif slider_value > 3:
        return "To balance privacy and accuracy, consider mid-range epsilon (>1 but <=3) and delta values (>10^{-7} but < 10^{-5}). Selecting these parameters requires great care. Work with a privacy expert to ensure the value of these parameters works well with your data."
    else:
        return "Maximize utility by using a larger privacy budget. Consider a larger epsilon value (>3 but <= 10) and a larger delta value (> 10^{-5} but <= 1/n where n is the size of your dataset). Selecting these parameters requires great care. Work with a privacy expert to ensure the value of these parameters works well with your data."

# --- DECISION FOREST NAVIGATION LOGIC ---
def ask_question(node):
    if isinstance(node, dict):
        question = list(node.keys())[0]
        options = list(node[question].keys())
        choice = st.radio(question, options)

        if st.button("Next", key=f"next_{question}"):
            st.session_state.history.append((question, choice))
            st.session_state.node = node[question][choice]
            st.rerun()
    else:
        if st.session_state.stage in ["main", "data_followup", "risk_followup"]:
            if st.session_state.stage == "data_followup" and not st.session_state.get("slider_submitted", False):
                st.subheader("Before we finalize your recommendation...")
                slider_value = st.slider(
                    "On a scale from 1 (Prioritize Accuracy) to 10 (Prioritize Privacy), what is your preference?",
                    min_value=1,
                    max_value=10,
                    value=5,
                    key="temp_slider_value"
                )

                if st.button("Submit Preference", key="submit_slider_preference"):
                    st.session_state.slider_answer = slider_value
                    st.session_state.history.append((
                        "Privacy vs Accuracy Preference",
                        f"{st.session_state.slider_answer}/10"
                    ))
                    st.session_state.slider_submitted = True
                    st.session_state.final_recommendation = node
                    st.rerun()
            else:
                if not st.session_state.summarize_recommendations:
                    if st.session_state.stage == "data_followup" and st.session_state.get("slider_submitted", True):
                        st.markdown("<h5>Our Recommendation</h5>", unsafe_allow_html=True)
                        st.success(get_slider_text(st.session_state.slider_answer) + node)
                    else:
                        st.markdown("<h5>Our Recommendation</h5>", unsafe_allow_html=True)
                        st.success(node)
                if st.session_state.stage == "main" and "Differential Privacy" in node:
                    st.subheader("Let's now determine how implementation details")
                    if st.button("Continue to Implementation Questions", key="privacy_budget"):
                        st.session_state.history.append(("Your privacy technology recommendation", node))
                        st.session_state.stage = "data_followup"
                        st.session_state.node = privacy_budget_decision_tree
                        st.session_state.slider_submitted = False
                        st.rerun()
                elif st.session_state.stage == "data_followup" or st.session_state.stage == "main":
                    st.subheader("Let's now understand the legal and policy considerations for your scenario")
                    if st.button("Continue to Legal Questions", key="risk_mitigation_button"):
                        if st.session_state.stage == "data_followup":
                            st.session_state.history.append(("Implementation Recommendations", get_slider_text(st.session_state.slider_answer) + node))
                        else:
                            st.session_state.history.append(("Your privacy technology recommendation", node))
                        st.session_state.stage = "risk_followup"
                        st.session_state.node = legal_decision_tree
                        st.session_state.final_recommendation = ""
                        st.session_state.slider_submitted = False
                        st.rerun()
                else:
                    if not st.session_state.summarize_recommendations:
                        if st.button("Summarize Tool Recommendations", key="summary_button"):
                            st.session_state.summarize_recommendations = True
                            st.session_state.history.append(("Legal and Policy Recommendations", node))
                            st.rerun()
                    else:
                        st.subheader("Summary of Privacy Technology Recommendations")
                        summaries = [entry for entry in st.session_state.history if
                                     "recommendation" in entry[0].lower()]
                        for title, recommendation in summaries:
                            st.markdown(f"**{title}**\n\n{recommendation}")
                            st.markdown("---")

                        if st.button("Restart", key="restart_button_final"):
                            st.session_state.node = decision_tree
                            st.session_state.history = []
                            st.session_state.stage = "main"
                            st.session_state.final_recommendation = ""
                            st.session_state.slider_submitted = False
                            st.session_state.summarize_recommendations = False
                            st.rerun()

# --- APP MAIN LOGIC ---
st.write("Welcome to the Privacy Tool! Answer the below questions to understand what privacy tool would be the best fit for your data usage scenario!")

if st.session_state.history:
    history_html = "<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px;'><h5>Your Choices So Far:</h5>"
    for q, a in st.session_state.history:
        history_html += f"<p><strong>{q}</strong> → <em>{a}</em></p>"
    history_html += "</div>"
    st.markdown(history_html, unsafe_allow_html=True)

# Ask the next question or show the final answer
ask_question(st.session_state.node)
