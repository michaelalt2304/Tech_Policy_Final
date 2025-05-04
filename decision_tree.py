# --- DECISION TREES ---
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
                        "Numerical": "Central Differential Privacy (DP) with the Laplace Mechanism\n\nCentral DP with the Laplace Mechanism protects individual data as a rigorous mathematical tool adding calibrated noise to aggregate query results. The Laplace mechanism is a natural fit for numeric queries (like counts or sums), as it ensures differential privacy by adding noise proportional to the query’s sensitivity. This approach is well-suited here because the data is centrally collected and can be processed in a secure environment, enabling accurate analytics while protecting individual privacy.",  # LEAF
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
                        "Yes": "Use a small epsilon (<=1) and consider a regular budget refresh.\n\nSince new data will be continuously entering the system and the user expects to make ongoing queries, a regular privacy budget refresh helps maintain utility over time without compromising long-term privacy. A small epsilon (≤ 1) is recommended to prioritize strong privacy guarantees, keeping individual data contributions highly protected even in the presence of repeated access. This balance allows for responsible, privacy-preserving analytics at scale.", # LEAF
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

# Decision tree for legal/policy recommendations
legal_decision_tree = {
    "Will you be processing data from and/or in any of the these regions?": {
        "European Union" : {
            "Does your data include personal data?": {
                "Yes" : "GDPR",
                "No" : "No recommendation"
            }
        }, # GDPR if personal data
        "United States" : {
            "Does your business reside in California?": {
                "Yes": {
                    "Do you satisfy at least one of the following: \n 1) have >$25 million in annual gross revenue\n 2) handle data of >50 000 California residents\n 3) receive over half your revenue from selling California resident personal data": {
                        "Yes": {
                            "Does your data include personal data?": {
                                "Yes": {
                                    "Are you handling data containing medical records or. educational records?": { #USA QUESITONS
                                        "Medical": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA + HIPAA + CCPA",
                                                "No" : "No recommendation"
                                            }
                                        },
                                        "Educational ": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA + FERPA + CCPA",
                                                "No" : "No recommendation"
                                            },
                                        },
                                        "Neither": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA + CCPA",
                                                "No" : "No recommendation"
                                            }
                                        }
                                    }
                                },  # CCPA + GDPR
                                "No": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA",
                                        "No": "No recommendation"
                                    }
                                }
                            }
                        },
                        "No" : {
                            "Are you handling data containing medical records or educational records?": { #USA QUESITONS
                                "Medical": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA + HIPAA",
                                        "No" : "No recommendation"
                                    }
                                },
                                "Educational ": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA + FERPA",
                                        "No" : "No recommendation"
                                    },
                                },
                                "Neither": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA",
                                        "No" : "No recommendation"
                                    }
                                }
                            }
                        }
                    }
                },
                "No" : {
                    "Are you handling data containing medical records or educational records?": {  # USA QUESITONS
                        "Medical": {
                            "Are you handling data of minors (children under the age of 13)?": {
                                "Yes": "COPPA + HIPAA",
                                "No": "No recommendation"
                            }
                        },
                        "Educational ": {
                            "Are you handling data of minors (children under the age of 13)?": {
                                "Yes": "COPPA + FERPA",
                                "No": "No recommendation"
                            },
                        },
                        "Neither": {
                            "Are you handling data of minors (children under the age of 13)?": {
                                "Yes": "COPPA",
                                "No": "No recommendation"
                            }
                        }
                    }
                }
            }
        },
        "Both" :{
            "Does your business reside in California?": {
                "Yes": {
                    "Do you satisfy at least one of the following: \n 1) have >$25 million in annual gross revenue \n 2) handle data of >50 000 California residents \n 3) receive over half your revenue from selling California resident personal data": {
                        "Yes": {
                            "Does your data include personal data?": {
                                "Yes": {
                                    "Are you handling data containing medical records or. educational records?": { #USA QUESITONS
                                        "Medical": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA + HIPAA + CCPA + GDPR",
                                                "No" : "No recommendation"
                                            }
                                        },
                                        "Educational ": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA + FERPA + CCPA + GDPR",
                                                "No" : "No recommendation"
                                            },
                                        },
                                        "Neither": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA + CCPA + GDPR",
                                                "No" : "No recommendation"
                                            }
                                        }
                                    }
                                },  # CCPA + GDPR
                                "No": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA",
                                        "No": "No recommendation"
                                    }
                                }
                            }
                        },
                        "No": {
                            "Does your data include personal data?": {
                                "Yes": {
                                    "Are you handling data containing medical records or. educational records?": {
                                        # USA QUESITONS
                                        "Medical": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA + HIPAA + GDPR",
                                                "No": "No recommendation"
                                            }
                                        },
                                        "Educational ": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA + FERPA + GDPR",
                                                "No": "No recommendation"
                                            },
                                        },
                                        "Neither": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA + GDPR",
                                                "No": "No recommendation"
                                            }
                                        }
                                    }
                                },  # GDPR
                                "No": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA",
                                        "No": "No recommendation"
                                    }
                                }
                            }
                        }
                    }
                },
                "No": {
                    "Does your data include personal data?": {
                        "Yes": {
                            "Are you handling data containing medical records or. educational records?": {
                                # USA QUESITONS
                                "Medical": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA + HIPAA + GDPR",
                                        "No": "No recommendation"
                                    }
                                },
                                "Educational ": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA + FERPA + GDPR",
                                        "No": "No recommendation"
                                    },
                                },
                                "Neither": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA + GDPR",
                                        "No": "No recommendation"
                                    }
                                }
                            }
                        },  # GDPR
                        "No": {
                            "Are you handling data of minors (children under the age of 13)?": {
                                "Yes": "COPPA",
                                "No": "No recommendation"
                            }
                        }
                    }
                }
            }
        },
        "Neither" : "No recommendation"
    }
}