# --- DECISION TREES ---
decision_tree = {
    "How will you use your data?": {
        "Answer questions about the data": {
            "How is your data stored?": {
                "Locally": {
                    "Do you want to jointly compute a publicly-known function without sharing any raw, noised data?": {
                        "Yes": "Secure Multi-Party Computation (MPC)\n\n Why it's suggested: You want to compute a function across locally stored datasets without revealing any raw or noisy data. \n\n What it is: Secure MPC lets multiple parties jointly compute a function (like a sum or multiplication) without any party learning others' raw inputs. \n\n How: Each party splits their data into random shares and sends them to other parties. These shares are used to evaluate the function securely. No single party can reconstruct the raw data, but the final output is correct and can be openly shared.", #LEAF
                        "No": {
                            "Do you have a trusted analyst to process the data and a trusted location to store the data centrally?": {
                                "Yes": {
                                    "What do you prioritize more?": {
                                        "Accuracy": {
                                            "What kinds of questions do you want to answer?": {
                                                "Numerical": "Central Differential Privacy with Laplace Mechanism \n\n Why it's suggested: You store your data locally, but have a trusted analyst that can collect the data centrally and process it. You prioritize accuracy and central differential privacy has higher accuracy because it adds less noise. You want to answer numerical, population-level queries about your data. \n\n What it is: A method for adding noise to numeric query results to ensure privacy. \n\n  How: After collecting your data and computing a numerical statistic like count or average, you add noise sampled from the Laplace distribution. The amount of noise depends on the sensitivity of the query and your privacy budget ε. For example, if each user can only contribute once, sensitivity is 1, and you add Lap(1/ε) noise. ", #LEAF
                                                "Categorical": "Central DP with Exponential Mechanism \n\n Why it's suggested: You store your data locally, but have a trusted analyst that can collect the data centrally and process it. You prioritize accuracy and central differential privacy has higher accuracy because it adds less noise. You want to answer categorical, population-level queries about your data. \n\n What it is: A DP mechanism that selects from among discrete options (like labels or categories) based on a utility score. \n\n How: Each possible answer is assigned a score, and results are sampled with a probability proportional to exp(ε × score / (2 × sensitivity)). You define the scoring function, compute the probabilities, and sample accordingly. " #LEAF
                                            }
                                        },
                                        "Privacy": {
                                            "What kinds of questions do you want to answer?": {
                                                "Numerical": "Local DP with Laplace Mechanism \n\n Why it's suggested: Your data is stored locally or on device, and you're prioritizing privacy for numerical, population-level queries. \n\n What it is: Users add noise to their own data before sending it to the server. \n\n How: Each user computes the answer (e.g., number of app uses) and adds laplace noise locally. These noisy results are sent to a server, which aggregates them. This method ensures privacy without needing to trust the server.",  # LEAF
                                                "Categorical": "Local DP with Exponential Mechanism \n\n Why it's suggested: Your data is stored locally or on device, and are answering categorical, population-level questions. \n\n What it is: A local method where users probabilistically report answers based on a private scoring function. \n\n How: Each possible answer is assigned a score, and results are sampled with a probability proportional to exp(ε × score / (2 × sensitivity)). Each user computes utility scores for all options and samples one. The noisy choice is sent to the server, which aggregates results from all users. This method ensures privacy without needing to trust the server."  # LEAF
                                            }
                                        }
                                    }
                                },
                                "No": {
                                    "What kinds of questions do you want to answer?": {
                                        "Numerical": "Local DP with Laplace Mechanism \n\n Why it's suggested: Your data is stored locally or on device, and you're prioritizing privacy for numerical, population-level queries. \n\n What it is: Users add noise to their own data before sending it to the server. \n\n How: Each user computes the answer (e.g., number of app uses) and adds laplace noise locally. These noisy results are sent to a server, which aggregates them. This method ensures privacy without needing to trust the server.", #LEAF
                                        "Categorical": "Local DP with Exponential Mechanism \n\n Why it's suggested: Your data is stored locally or on device, and are answering categorical, population-level questions. \n\n What it is: A local method where users probabilistically report answers based on a private scoring function. \n\n How: Each possible answer is assigned a score, and results are sampled with a probability proportional to exp(ε × score / (2 × sensitivity)). Each user computes utility scores for all options and samples one. The noisy choice is sent to the server, which aggregates results from all users. This method ensures privacy without needing to trust the server." #LEAF
                                    }
                                }
                            }
                        }
                    }
                },
                "Centrally": {
                    "What kinds of questions do you want to answer?": {
                        "Numerical": "Central Differential Privacy with Laplace Mechanism \n\n Why it's suggested: You store your data centrally, and want to answer numerical, population-level queries about your data. \n\n What it is: A method for adding noise to numeric query results to ensure privacy. \n\n How: After collecting your data and computing a numerical statistic like count or average, you add noise sampled from the Laplace distribution. The amount of noise depends on the sensitivity of the query and your privacy budget ε. For example, if each user can only contribute once, sensitivity is 1, and you add Lap(1/ε) noise.",  # LEAF
                        "Categorical": "Central DP with Exponential Mechanism \n\n Why it's suggested: You store data centrally and want to use it to answer categorical, population-level queries about your data. \n\n What it is: A DP mechanism that selects from among discrete options (like labels or categories) based on a utility score. \n\n How: Each possible answer is assigned a score, and results are sampled with a probability proportional to exp(ε × score / (2 × sensitivity)). You define the scoring function, compute the probabilities, and sample accordingly." # LEAF
                    }
                }
            }
        },
        "Send it privately to other parties": {
             "Do you have a pre-shared private key?": {
                "Yes": "Private-Key Cryptography \n\n Why it's suggested: You’re sending private data and have already shared a private key with the recipient. \n\n What it is: A method of encrypting and decrypting data with the same shared secret key. \n\n How: Using your secure private key, encrypt messages and send them to the other party. The recipient uses the same key to decrypt the message.", #LEAF
                "No": "Public-Key Cryptography \n\n Why it's suggested: You’re sending private data and do not have a shared private key in advance. \n\n What it is: A method where each person has a public and private key pair. You encrypt with one and decrypt with the other. \n\n How: The recipient creates a public and private key pair. Encrypt the message using the recipient's public key. Only the recipient can decrypt it with their private key." #LEAF
            }
        },
        "Publicly release it": {
             "How will the released data be used?": {
                "Answer a pre-specified query set": "Synthetic Data with Private GANs \n\n Why it's suggested: You’re releasing data publicly to answer a pre-specified set of queries. \n\n What it is: A GAN (Generative Adversarial Network) employs two competing neural networks to generate data. One network is the Generator that generates synthetic data and the other is the Discriminator that learns how to differentiate between the synthetic and true data. \n\n How: Train a GAN where the generator and discriminator improve via adversarial learning. To make it private, you use Differentially Private Stochastic Gradient Descent (DP-SGD), clipping gradient norms and adding Gaussian noise during training. This prevents overfitting to individual records. After training, you publish only the generator.  \n\n *Warning*: You might be tempted to use anonymization, since it is a commonly used approach when sharing data. Do not assume anonymization (removing names or IDs) provides privacy. Re-identification attacks can match “de-identified” records with external data.", #LEAF
                "Answer unknown queries": "Synthetic Data with Exponential Mechanism \n\n Why it's suggested: You want to publicly release data that may be used to answer many or unknown future queries. \n\n What it is: You create synthetic datasets by scoring candidate datasets and sampling from them in a DP-compliant way. \n\n How: Define a utility score that captures how well a synthetic dataset preserves accuracy across many possible queries. Then, use the exponential mechanism to probabilistically sample synthetic outputs, with higher-quality ones more likely. This approach is suitable when strong privacy guarantees are required. \n\n *Warning*: You might be tempted to use anonymization, since it is a commonly used approach when sharing data. Do not assume anonymization (removing names or IDs) provides privacy. Re-identification attacks can match “de-identified” records with external data. Formal DP is necessary to provide robust privacy guarantees." #LEAF
            }
        },
        "Train an ML model": {
            "How is your data being stored?": {
                "Centrally": "Central Differentially Private Machine Learning \n\n Why it's suggested: You want to train a machine learning model on centrally stored data while protecting the privacy of individual contributions. \n\n What it is: Differentially Private Machine Learning training. \n\n How: At each training step, per-example gradients are clipped, and laplace noise is added before applying updates. This helps prevent the model from memorizing individual training data. ", #LEAF
                "Locally": {
                    "Do you have a trusted secure server?": {
                        "Yes":  "Federated Learning with Secure Multi-Party Computation and Central Differential Privacy \n\n Why it's suggested: Your data is stored locally, you don’t have a trusted server, have significant computational resources and want to prioritize accuracy. \n\n What it is: Federated learning lets users compute model updates locally. Users then leverage MPC to securely compute the average of model updates, followed by central DP. \n\n How: After computing updates locally, each client splits their model updates into secret shares, sent to aggregators that jointly compute the global update without ever seeing raw values. DP noise is then added. This approach offers privacy without trusting any single party. ", #LEAF
                        "No": {
                            "What do you prioritize more?": {
                                "Accuracy": "Federated Learning with Secure Multi-Party Computation and Central Differential Privacy \n\n Why it's suggested: Your data is stored locally, you don’t have a trusted server, have significant computational resources and want to prioritize accuracy. \n\n What it is: Federated learning lets users compute model updates locally. Users then leverage MPC to securely compute the average of model updates, followed by central DP. \n\n How: After computing updates locally, each client splits their model updates into secret shares, sent to aggregators that jointly compute the global update without ever seeing raw values. DP noise is then added. This approach offers privacy without trusting any single party. ", #LEAF
                                "Privacy and computational efficiency": "Federated Learning with Local Differential Privacy \n\n Why it's suggested: Your data is stored locally, you don’t trust a central server and prioritize privacy or computation efficiency. \n\n What it is: Federated learning lets users compute model updates locally. Each client then adds DP noise to its local model updates before sending them to the server. \n\n How: During training, users add noise to their local gradients or parameters. The server aggregates these noisy updates to update the model. This is lightweight and avoids the need for secure aggregation but can affect accuracy." #LEAF
                            }
                        }
                    }
                }
            }
        },
        "Verify data integrity":{
            "What would you like to verify?": {
                "Authenticity and integrity of the data": "Digital Signatures \n\n Why it's suggested: You want to verify authenticity and integrity of data. \n\n What it is: A cryptographic method where data is signed with a private key and verified with a public key. \n\n How: You hash the message and sign the hash using your private key. Anyone with your public key can verify the signature matches the content. This ensures the data hasn’t been altered and that it came from the expected source. ",  # LEAF
                "Data hasn't been tampered with": "Cryptographic Hash Functions \n\n Why it's suggested: You want to verify that data hasn’t been tampered with. \n\n What it is: A hash function outputs a fixed-size digest that changes drastically with small changes in input. \n\n How: Before storing or sending data, compute its hash. Later, re-compute the hash and compare to the original. If they match, the data hasn’t changed. "  # LEAF
            }
        }
    }
}

# Define the secondary decision tree for privacy budget allocation
privacy_budget_decision_tree = {
    "Will multiple separate parties be asking questions about the data?": {
        "No": {
            "How many queries will you need to make?": {
                "Finite": "Maintain a fixed privacy budget over time to limit cumulative privacy loss. Since data isn’t being refreshed, budget refreshes could risk privacy leaks and should be avoided if possible.", # LEAF
                "Infinite": {
                    "Will new data enter your dataset and old data retire?": {
                        "Yes": "Periodically renew the privacy budget to support ongoing analysis and account for the incoming data.", # LEAF
                        "No": "Maintain a fixed privacy budget over time to limit cumulative privacy loss. Since data isn’t being refreshed, budget refreshes could risk privacy leaks and should be avoided if possible." # LEAF
                    }
                }
            }
        },
        "Yes": {
            "Can you trust that these parties won’t collude? For example, will they share the results of their queries.": {
                "Yes": {
                    "How many times will you need to query your data?": {
                        "Finite": "Maintain a fixed privacy budget over time to limit cumulative privacy loss. Since data isn’t being refreshed, budget refreshes could risk privacy leaks and should be avoided if possible.", # LEAF
                        "Infinite": {
                            "Will new data enter your dataset and old data retire?": {
                                "Yes": "Periodically renew the privacy budget to support ongoing analysis and account for the incoming data.", # LEAF
                                "No": "Maintain a fixed privacy budget over time to limit cumulative privacy loss. Since data isn’t being refreshed, budget refreshes could risk privacy leaks and should be avoided if possible." # LEAF
                            }
                        }
                    }
                },
                "No": {
                    "How many queries will you need to make?": {
                        "Finite": "Maintain a fixed privacy budget over time to limit cumulative privacy loss. Since data isn’t being refreshed, budget refreshes could risk privacy leaks and should be avoided if possible.", # LEAF
                        "Infinite": {
                            "Will new data enter your dataset and old data retire?": {
                                "Yes": "Periodically renew the privacy budget to support ongoing analysis and account for the incoming data. Reduce the privacy budget allocated to each entity to enhance overall privacy protections, to ensure privacy is still protected if entities collude.", # LEAF
                                "No": "Maintain a fixed privacy budget over time to limit cumulative privacy loss. Since data isn’t being refreshed, budget refreshes could risk privacy leaks and should be avoided if possible. Reduce the privacy budget allocated to each entity to enhance overall privacy protections, to ensure privacy is still protected if entities collude." # LEAF
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
                "Yes" : "GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.",
                "No" : ""
            }
        }, # GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data. if personal data
        "United States" : {
            "Do you do business in California?": {
                "Yes": {
                    "Do you satisfy at least one of the following: \n 1) have >$25 million in annual gross revenue\n 2) handle data of >50 000 California residents\n 3) receive over half your revenue from selling California resident personal data": {
                        "Yes": {
                            "Does your data include personal data?": {
                                "Yes": {
                                    "Are you handling data containing medical records or educational records?": { #USA QUESITONS
                                        "Medical": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n HIPAA (Health Insurance Portability and Accountability Act): U.S. law that safeguards medical information; sets standards for data privacy, security, and breach notifications in healthcare. \n\n CCPA (California Consumer Privacy Act): California law granting residents rights over personal data, including access, deletion, and opting out of sale; applies to certain businesses. ",
                                                "No" : ""
                                            }
                                        },
                                        "Educational ": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n FERPA (Family Educational Rights and Privacy Act): U.S. law that protects the privacy of student education records; gives parents and eligible students rights over access and correction.  \n\n CCPA (California Consumer Privacy Act): California law granting residents rights over personal data, including access, deletion, and opting out of sale; applies to certain businesses. ",
                                                "No" : ""
                                            },
                                        },
                                        "Neither": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n CCPA (California Consumer Privacy Act): California law granting residents rights over personal data, including access, deletion, and opting out of sale; applies to certain businesses. ",
                                                "No" : ""
                                            }
                                        },
                                        "Both": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "HIPPA \n\n FERPA (Family Educational Rights and Privacy Act): U.S. law that protects the privacy of student education records; gives parents and eligible students rights over access and correction.  \n\n COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n CCPA (California Consumer Privacy Act): California law granting residents rights over personal data, including access, deletion, and opting out of sale; applies to certain businesses. ",
                                                "No" : ""
                                            }
                                        }
                                    }
                                },  # CCPA (California Consumer Privacy Act): California law granting residents rights over personal data, including access, deletion, and opting out of sale; applies to certain businesses.  \n\n GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.
                                "No": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices.",
                                        "No": ""
                                    }
                                }
                            }
                        },
                        "No" : {
                            "Are you handling data containing medical records or educational records?": { #USA QUESITONS
                                "Medical": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n HIPAA (Health Insurance Portability and Accountability Act): U.S. law that safeguards medical information; sets standards for data privacy, security, and breach notifications in healthcare.",
                                        "No" : ""
                                    }
                                },
                                "Educational ": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n FERPA (Family Educational Rights and Privacy Act): U.S. law that protects the privacy of student education records; gives parents and eligible students rights over access and correction. ",
                                        "No" : ""
                                    },
                                },
                                "Neither": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices.",
                                        "No" : ""
                                    }
                                },
                                    "Both": {
                                        "Are you handling data of minors (children under the age of 13)?": {
                                            "Yes": "HIPPA \n\n FERPA (Family Educational Rights and Privacy Act): U.S. law that protects the privacy of student education records; gives parents and eligible students rights over access and correction.  \n\n COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices.",
                                            "No" : ""
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
                                "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n HIPAA (Health Insurance Portability and Accountability Act): U.S. law that safeguards medical information; sets standards for data privacy, security, and breach notifications in healthcare.",
                                "No": ""
                            }
                        },
                        "Educational ": {
                            "Are you handling data of minors (children under the age of 13)?": {
                                "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n FERPA (Family Educational Rights and Privacy Act): U.S. law that protects the privacy of student education records; gives parents and eligible students rights over access and correction. ",
                                "No": ""
                            },
                        },
                        "Neither": {
                            "Are you handling data of minors (children under the age of 13)?": {
                                "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices.",
                                "No": ""
                            }
                        },
                        "Both": {
                            "Are you handling data of minors (children under the age of 13)?": {
                                "Yes": "HIPPA \n\n FERPA (Family Educational Rights and Privacy Act): U.S. law that protects the privacy of student education records; gives parents and eligible students rights over access and correction.  \n\n COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices.",
                                "No" : ""
                            }
                        }
                    }
                }
            }
        },
        "Both" :{
            "Do you do business in California?": {
                "Yes": {
                    "Do you satisfy at least one of the following: \n 1) have >$25 million in annual gross revenue \n 2) handle data of >50 000 California residents \n 3) receive over half your revenue from selling California resident personal data": {
                        "Yes": {
                            "Does your data include personal data?": {
                                "Yes": {
                                    "Are you handling data containing medical records or. educational records?": { #USA QUESITONS
                                        "Medical": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n HIPAA (Health Insurance Portability and Accountability Act): U.S. law that safeguards medical information; sets standards for data privacy, security, and breach notifications in healthcare. \n\n CCPA (California Consumer Privacy Act): California law granting residents rights over personal data, including access, deletion, and opting out of sale; applies to certain businesses.  \n\n GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.",
                                                "No" : ""
                                            }
                                        },
                                        "Educational ": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n FERPA (Family Educational Rights and Privacy Act): U.S. law that protects the privacy of student education records; gives parents and eligible students rights over access and correction.  \n\n CCPA (California Consumer Privacy Act): California law granting residents rights over personal data, including access, deletion, and opting out of sale; applies to certain businesses.  \n\n GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.",
                                                "No" : ""
                                            },
                                        },
                                        "Neither": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n CCPA (California Consumer Privacy Act): California law granting residents rights over personal data, including access, deletion, and opting out of sale; applies to certain businesses.  \n\n GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.",
                                                "No" : ""
                                            }
                                        },
                                        "Both": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "HIPPA \n\n FERPA (Family Educational Rights and Privacy Act): U.S. law that protects the privacy of student education records; gives parents and eligible students rights over access and correction.  \n\n COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n CCPA (California Consumer Privacy Act): California law granting residents rights over personal data, including access, deletion, and opting out of sale; applies to certain businesses.  \n\n GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.",
                                                "No" : ""
                                            }
                                        }
                                    }
                                },  # CCPA (California Consumer Privacy Act): California law granting residents rights over personal data, including access, deletion, and opting out of sale; applies to certain businesses.  \n\n GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.
                                "No": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices.",
                                        "No": ""
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
                                                "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n HIPAA (Health Insurance Portability and Accountability Act): U.S. law that safeguards medical information; sets standards for data privacy, security, and breach notifications in healthcare. \n\n GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.",
                                                "No": ""
                                            }
                                        },
                                        "Educational ": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n FERPA (Family Educational Rights and Privacy Act): U.S. law that protects the privacy of student education records; gives parents and eligible students rights over access and correction.  \n\n GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.",
                                                "No": ""
                                            },
                                        },
                                        "Neither": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.",
                                                "No": ""
                                            }
                                        },
                                        "Both": {
                                            "Are you handling data of minors (children under the age of 13)?": {
                                                "Yes": "HIPPA \n\n FERPA (Family Educational Rights and Privacy Act): U.S. law that protects the privacy of student education records; gives parents and eligible students rights over access and correction.  \n\n COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.",
                                                "No" : ""
                                            }
                                        }
                                    }
                                },  # GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.
                                "No": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices.",
                                        "No": ""
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
                                        "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n HIPAA (Health Insurance Portability and Accountability Act): U.S. law that safeguards medical information; sets standards for data privacy, security, and breach notifications in healthcare. \n\n GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.",
                                        "No": ""
                                    }
                                },
                                "Educational ": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n FERPA (Family Educational Rights and Privacy Act): U.S. law that protects the privacy of student education records; gives parents and eligible students rights over access and correction.  \n\n GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.",
                                        "No": ""
                                    },
                                },
                                "Neither": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.",
                                        "No": ""
                                    }
                                },
                                "Both": {
                                    "Are you handling data of minors (children under the age of 13)?": {
                                        "Yes": "HIPPA \n\n FERPA (Family Educational Rights and Privacy Act): U.S. law that protects the privacy of student education records; gives parents and eligible students rights over access and correction.  \n\n COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices. \n\n GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.",
                                        "No" : ""
                                    }
                                }
                            }
                        },  # GDPR (General Data Protection Regulation): European Union regulation providing strong data protection rights, including consent, access, erasure, and data portability; applies globally if processing EU resident data.
                        "No": {
                            "Are you handling data of minors (children under the age of 13)?": {
                                "Yes": "COPPA (Children’s Online Privacy Protection Act): U.S. law that restricts the collection and use of personal data from children under 13; requires parental consent and clear privacy notices.",
                                "No": ""
                            }
                        }
                    }
                }
            }
        },
        "Neither" : ""
    }
}