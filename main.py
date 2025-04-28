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

st.header("Privacy Tool")
st.subheader("Policy for Privacy Technology Final Project")
st.text("By: Brigid, Michael, Alison, Brittany")

# Define the decision tree as a nested dictionary
decision_tree = {
    "How will you use your data?": {
        "Answer questions about the data": {
            "How is your data stored?": {
                "Locally": {
                    "Do you want to jointly comput a publically-known function without sharing any raw, noised data?": {
                        "Yes": "Secure MPC", #LEAF
                        "No": {
                            "Do you have a trusted analyst to process the data and a trusted location to store the data centrally?": {
                                "Yes": {
                                    "What do you prioritize more?": {
                                        "Accuracy": {
                                            "What kinds of questions do you want to answer?": {
                                                "Numerical": "Central DP with Laplace Mechanism", #LEAF
                                                "Categorical": "Central DP with Exponential Mechanism" #LEAF
                                            }
                                        },
                                        "Privacy": {
                                            "What kinds of questions do you want to answer?": {
                                                "Numerical": "Local DP with Laplace Mechanism",  # LEAF
                                                "Categorical": "Local DP with Exponential Mechanism"  # LEAF
                                            }
                                        }
                                    }
                                },
                                "No": {
                                    "What kinds of questions do you want to answer?": {
                                        "Numerical": "Local DP with Laplace Mechanism", #LEAF
                                        "Categorical": "Local DP with Exponential Mechanism" #LEAF
                                    }
                                }
                            }
                        }
                    }
                },
                "Centrally": {
                    "What kinds of questions do you want to answer?": {
                        "Numerical": "Central DP with Laplace Mechanism",  # LEAF
                        "Categorical": "Central DP with Exponential Mechanism" # LEAF
                    }
                }
            }
        },
        "Send it privately to other parties": {
             "Do you have a pre-shared private key?": {
                "Yes": "Private-key cryptography", #LEAF
                "No": "Public-key cryptography" #LEAF
            }
        },
        "Publicly release it": {
             "How will the released data be used?": {
                "Answer a pre-specified query set": "Generate synthetic data with private GANS", #LEAF
                "Answer unknown queries": "Generate synthetic data with the exponential mechanism" #LEAF
            }
        },
        "Train an ML model": {
            "How is your data being stored?": {
                "Centrally": "Central DP-ML", #LEAF
                "Locally": {
                    "Do you have a trusted secure server?": {
                        "Yes":  "Federated learning with secure server + central DP", #LEAF
                        "No": {
                            "What do you prioritize more?": {
                                "Accuracy": "Federated learning with MPC + Central DP", #LEAF
                                "Privacy and computational efficiency": "Federated learning with local DP" #LEAF
                            }
                        }
                    }
                }
            }
        },
        "Verify data integrity":{
            "What would you like to verify?": {
                "Authenticity and integrity of the data": "Digital signatures",  # LEAF
                "Data hasn't been tampered with": "Cryptographic hash functions"  # LEAF
            }
        }
    }
}

# Define the secondary decision tree for privacy budget allocation
privacy_budget_decision_tree = {
    "Will multiple separate parties be asking questions about the data?": {
        "No": {
            "How many queries will you need to make?": {
                "Finite": "A fixed budget with no budget refreshes.", # LEAF
                "Infinite": {
                    "Will new data enter your dataset and old data retire?": {
                        "Yes": "A regular budget refresh to account for the new data.", # LEAF
                        "No": "A fixed budget with no budget refreshes." # LEAF
                    }
                }
            }
        },
        "Yes": {
            "Can you trust that these parties won’t collude? For example, will they share the results of their queries.": {
                "Yes": {
                    "How many queries will you need to make?": {
                        "Finite": "A fixed budget with no budget refreshes.", # LEAF
                        "Infinite": {
                            "Will new data enter your dataset and old data retire?": {
                                "Yes": "A regular budget refresh to account for the new data. Decreased budget per party that handles the data.", # LEAF
                                "No": "A fixed budget with no budget refreshes. Decreased budget per party that handles the data." # LEAF
                            }
                        }
                    }
                },
                "No": {
                    "How many queries will you need to make?": {
                        "Finite": "A fixed budget with no budget refreshes.", # LEAF
                        "Infinite": {
                            "Will new data enter your dataset and old data retire?": {
                                "Yes": "A regular budget refresh to account for the new data. More budget allowed per party that handles the data.", # LEAF
                                "No": "A fixed budget with no budget refreshes. Decreased budget allowed per party that handles the data." # LEAF
                            }
                        }
                    }
                }
            }
        }
    }
}


# Add welcome text
st.write("Welcome to the Privacy Tool! Answer the below questions to understand what privacy tool would be the best fit for your data usage scenario!")

# Store session state to keep track of progress
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

# Function to display the current question or answer
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
        # Check if privacy budget needs to be allocated
        if st.session_state.stage == "main":
            st.session_state.final_recommendation = node
            st.session_state.show_first_recommendation = True
            st.rerun()
        else:
            # Before final recommendation in second tree, ask privacy budget question
            if not st.session_state.get("slider_submitted", False):
                st.subheader("Before we finalize your recommendation...")

                slider_value = st.slider(
                    "On a scale from 1 (Prioritize Privacy) to 10 (Prioritize Utility), what is your preference?",
                    min_value=1,
                    max_value=10,
                    value=5,
                    key="temp_slider_value"  # only widget manages this
                )

                if st.button("Submit Preference", key="submit_slider_preference"):
                    st.session_state.slider_answer = slider_value  # now read it from widget
                    st.session_state.history.append((
                        "Privacy vs Utility Preference",
                        f"{st.session_state.slider_answer}/10"
                    ))
                    st.session_state.slider_submitted = True
                    st.session_state.final_recommendation = node
                    st.rerun()
            else:
                recommendation_html = """
                    <h5>Our Recommendation</h5>
                    """
                st.markdown(recommendation_html, unsafe_allow_html=True)
                st.success(node)
                if st.button("Restart", key="restart_button_1"):
                    st.session_state.node = decision_tree
                    st.session_state.history = []
                    st.session_state.stage = "main"
                    st.session_state.final_recommendation = ""
                    st.session_state.show_first_recommendation = False
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

# Navigate the correct decision tree
if st.session_state.show_first_recommendation:
    recommendation_html = """
        <h5>Our Recommendation</h5>
        """
    st.markdown(recommendation_html, unsafe_allow_html=True)
    st.success(st.session_state.final_recommendation)
    if "DP" in st.session_state.final_recommendation:
        st.subheader("Let's now determine the privacy budget")
        if st.button("Continue to Privacy Budget Questions", key="privacy_budget"):
            st.session_state.history.append(("Your privacy technology recommendation", st.session_state.final_recommendation))
            st.session_state.stage = "data_followup"
            st.session_state.node = privacy_budget_decision_tree
            st.session_state.show_first_recommendation = False
            st.rerun()
    else:
        if st.button("Restart", key="restart_button_2"):
            st.session_state.node = decision_tree
            st.session_state.history = []
            st.session_state.stage = "main"
            st.session_state.final_recommendation = ""
            st.session_state.show_first_recommendation = False
            st.session_state.slider_submitted = False
            st.rerun()

# Ask the next question or show the final answer
ask_question(st.session_state.node)
