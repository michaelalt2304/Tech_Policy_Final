import streamlit as st
from openai import OpenAI

st.set_page_config("ProGuide", page_icon="🦈")
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

st.header("ProGuide")
st.subheader("Privacy in Policy Technology Final Project")
st.text("By: Brigid, Michael, Alison, Brittany")

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
    more = st.checkbox("Show all privacy implementation options?")
    submitted = st.form_submit_button("Generate advice!")
    


if submitted:
    with st.spinner("Compiling suggestions..."):
        prompt = "Please recommend some privacy technologies to me, in a short bulleted list with descriptions, with the following conditions: " + \
                    "Center the discussion around "
        prompt += "Use Synthetic Data, or Private GANs. Avoid k-anonymity/l-diversity unless heavily aggregated" if use_case == "I want to publish analysis results to the public" and (privacy == 5 or linked == False or not direct_PII) else \
                    "Differential Privacy (Central DP) for aggregated results. If no trust: use Local DP" if (trust >= 3 or curious >= 3) and use_case == "I want to publish analysis results to the public" else \
                    "Local DP" if trust <= 2 else \
                    "Use Public Key Cryptography for encryption. Optionally add Attestation for system-level trust" if use_case == "I need to send data to someone else" and direct_PII else \
                    "Use Homomorphic Encryption" if use_case == "I need another party to analyze data but not see raw data" and trust >= 3 else \
                    "Use Multi Party Encryption" if (use_case == "I need another party to analyze data but not see raw data" and  malicious >= 2) else \
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
    
    st.subheader("Below are technical specifications for how to implement your privacy technologies")
    
    stuff = False
    if (curious >= 3 and use_case == "I want to publish analysis results to the public" or trust <= 2) or (noise == True and use_case == "I need another party to analyze data but not see raw data" or use_case == "I am conducting analysis on data (locally or centrally)") or not use_case or more:
        expander_2 = st.expander("Local Differential Privacy")
        expander_2.write("Implementing Local Differential Privacy (LDP) technically, requires first identifying the data collection points (e.g., client devices or browsers) and applying noise to the data before it leaves the user’s device. This typically involves integrating an LDP mechanism—such as randomized response for binary or categorical data, or local hashing schemes like RAPPOR or Optimized Unary Encoding for larger domains—into the client-side codebase. For numeric data, you might use Laplace noise scaled according to the chosen privacy budget. A critical technical consideration is selecting an appropriate epsilon (ε), which controls the balance between privacy and data utility. Smaller ε values (e.g., <0.5) provide stronger privacy but introduce more noise, making aggregate analysis less precise, while higher values (e.g., 1–3) yield better utility but weaken privacy guarantees. Epsilon should be chosen based on the sensitivity of the data, the frequency of data collection, and the acceptable risk level, often informed by academic norms (e.g., ε ≈ 1 is common in deployed systems). It’s also essential to implement mechanisms like per-user query limits, memoization (to ensure the same input always results in the same noisy output), and cumulative privacy accounting to control total privacy loss over time. Data collected with LDP must be aggregated using statistical post-processing techniques (e.g., expectation-maximization or Bayesian denoising) to recover meaningful insights while respecting the privacy guarantees set by ε.")
        stuff = True
    if (trust >= 3 and use_case == "I want to publish analysis results to the public") or not use_case or more:
        expander_3 = st.expander("Centralized Differential Privacy")
        expander_3.write("To use Generalized Differential Privacy (GDP) in a technical system, you typically work within a centralized data collection model, where raw data is collected and privacy-preserving noise is added after aggregation or during query processing on the server side. The central idea is to ensure that the final output of any computation is differentially private, meaning the inclusion or exclusion of any single individual’s data does not significantly affect the result. This is achieved by applying mechanisms such as the Laplace or Gaussian mechanism, calibrated to a specified privacy parameter epsilon (ε) (and often delta, for approximate DP). The choice of epsilon is crucial: smaller values (e.g., ε ≤ 1) provide stronger privacy by adding more noise, while larger values (ε > 1) improve accuracy but reduce individual protection. In GDP, epsilon is chosen not only based on data sensitivity but also on how frequently queries are run and whether results are public-facing or internal. Additionally, GDP implementations require a privacy accountant to track cumulative privacy loss over multiple queries or time, especially in interactive systems. Technically, this involves maintaining a privacy budget for each user or dataset and halting or degrading results when the budget is exhausted. GDP can be integrated into systems through privacy-aware APIs (like Google's Differential Privacy libraries or Microsoft's SmartNoise), which wrap standard queries and inject noise based on predefined policies. Special care must be taken to avoid post-processing leaks or repeated queries on the same data, which can erode privacy. Finally, data engineers must document privacy configurations, epsilon values, and assumptions clearly to ensure compliance and transparency, particularly in regulated or ethical-sensitive environments.")
        stuff = True
    if (use_case == "I need to send data to someone else" and direct_PII) or not use_case or more:
        expander_4 = st.expander("Public-Key Encryption")
        expander_4.write("To implement Public Key Encryption (PKE) in a product or system, you begin by establishing a key pair—a public key and a corresponding private key—using a secure cryptographic algorithm such as RSA or Elliptic Curve Cryptography (ECC). The public key is distributed freely and used to encrypt data, while the private key is kept secret and used to decrypt that data. Technically, this is often handled through a Public Key Infrastructure (PKI), which manages certificate issuance and validation via a trusted Certificate Authority (CA). The encryption process starts with key generation, typically performed with a cryptographic library (e.g., OpenSSL, WebCrypto, or Python’s cryptography library), and secure storage of the private key in a hardware security module (HSM) or a secure key vault. Public keys are embedded into the client application, transferred over HTTPS, or provided via certificates. In practice, public key encryption is often used in a hybrid model—it encrypts a symmetric session key (like AES), which is then used to encrypt the actual data payload, combining the efficiency of symmetric encryption with the security of asymmetric key exchange. This approach is core to TLS/SSL, secure messaging, and file encryption systems. Proper implementation also includes managing key rotation, validating certificate chains, applying secure padding schemes (like OAEP for RSA), and defending against attacks such as man-in-the-middle or key substitution. Finally, all cryptographic operations must be audited, and access to keys strictly controlled, to ensure end-to-end confidentiality and authenticity within the system.")
        stuff = True
    if (use_case == "I need another party to analyze data but not see raw data" and trust >= 3) or not use_case or more:
        expander_5 = st.expander("Homomorphic Encryption")
        expander_5.write("Homomorphic Encryption (HE) is applied to a problem by first selecting an appropriate HE scheme based on your use case—Partially Homomorphic Encryption (PHE) for limited operations like addition or multiplication, or Fully Homomorphic Encryption (FHE) if you need to support arbitrary computations on encrypted data. Common libraries such as Microsoft SEAL, PALISADE, or HElib provide robust cryptographic backends for these schemes. The implementation begins with generating a public/private key pair, where the public key is used to encrypt data on the client or a trusted party’s system, and the private key is retained securely by the data owner to decrypt the final results. The encrypted data, often represented as ciphertexts containing complex algebraic structures (e.g., polynomials), is then sent to an untrusted server or cloud for computation. What makes HE unique is that the server performs computations directly on the ciphertexts, and when the result is decrypted, it matches what would have been obtained from computing on the original plaintexts. Choosing encryption parameters like the polynomial modulus degree, coefficient modulus, and plaintext modulus is critical—they determine the trade-off between security, performance, and the size of supported computations. HE is computationally intensive and may introduce significant latency and memory overhead, so optimizations like batching, relinearization, and ciphertext modulus switching are often used. Additionally, managing key distribution securely, preventing ciphertext reuse, and monitoring noise growth (which can eventually corrupt ciphertexts) are important operational concerns. While still maturing, HE enables powerful privacy-preserving applications such as secure machine learning inference, encrypted search, and outsourced analytics without ever exposing sensitive user data.")
        stuff = True
    if (use_case == "I need another party to analyze data but not see raw data" and malicious >= 2) or (use_case == "I want to publish analysis results to the public" and malicious > 3) or not use_case or more:
        expander_6 = st.expander("Multi Party Encryption")
        expander_6.write("Multi-Party Encryption—often referring to Secure Multi-Party Computation (MPC) or cryptographic protocols that involve threshold encryption or distributed key management—you begin by designing a protocol where multiple parties can jointly compute a function or decrypt a message without any single party learning the full input or key. In a typical MPC setup, each participant holds a secret share of the data or the decryption key, often generated through secret sharing schemes like Shamir’s Secret Sharing. These shares are distributed so that a predefined threshold (e.g., k of n parties) must collaborate to perform decryption or computation, enhancing resilience and privacy. Public parameters are generated collectively, and operations like addition or multiplication are performed on encrypted or shared values using protocols such as Yao’s Garbled Circuits for two-party settings or BGW/ SPDZ protocols for multi-party environments. Threshold encryption schemes (e.g., threshold RSA or Paillier) allow encryption using a public key, while decryption requires cooperation among multiple parties who each contribute a partial decryption share. Technically, this requires secure channels, commitment schemes, and often zero-knowledge proofs to ensure honest behavior. Libraries like MP-SPDZ, Sharemind, or FRESCO help implement these protocols securely and efficiently. Key considerations include minimizing communication overhead, ensuring scalability for many parties, and guarding against collusion or dropout. Use cases include secure voting, collaborative analytics, privacy-preserving machine learning, and decentralized key management in blockchain systems. MPC offers strong privacy without needing a trusted third party, but the trade-off is increased computational and protocol complexity, making careful cryptographic engineering and threat modeling essential.")
        stuff = True
    if (use_case == "I am conducting analysis on data (locally or centrally)" and noise == False) or (use_case == "I want to audit or verify system/data integrity") or not use_case or more:
        expander_7 = st.expander("Trusted Execution Environment")
        expander_7.write("using Trusted Execution Environments (TEE) starts by identifying sensitive code and data that need to be protected from unauthorized access, even from the operating system or hypervisor. TEEs, such as Intel SGX, ARM TrustZone, or AMD SEV, provide a secure enclave or isolated region of memory where this sensitive code can execute securely. Technically, you partition the application into a trusted component (running inside the TEE) and an untrusted component (running in the normal environment). The trusted component is compiled using a TEE-specific SDK—e.g., Intel SGX SDK or Open Enclave SDK—which ensures it can only run within the enclave and interact with external systems via secure calls (ECALLs and OCALLs). The data enters the TEE either through encrypted channels or secure APIs, and all memory and computations inside the enclave are protected with hardware-enforced isolation and encryption. Developers must carefully design the interface between trusted and untrusted code to minimize the attack surface, avoid side-channel vulnerabilities, and ensure that sensitive operations (e.g., key management, cryptographic operations, ML inference) are performed exclusively inside the TEE. Additionally, TEEs support remote attestation, allowing a remote party to verify that a genuine, untampered enclave is executing specific code before sharing sensitive inputs. Key management must be tightly controlled, often using sealed storage, where encrypted secrets are bound to the specific enclave. While TEEs offer strong guarantees, they require careful attention to memory limits, threat modeling, and vendor-specific security advisories. They're especially useful for secure data analytics, confidential AI, DRM, and blockchain key custody, where trust must be established even in potentially hostile environments.")
        stuff = True
    if use_case == "I want to audit or verify system/data integrity" or not use_case or more:
        expander_8 = st.expander("Attestation")
        expander_8.write("With attestation—especially in the context of trusted computing or confidential computing—you start by enabling a mechanism that allows a remote or local party to verify the integrity and authenticity of a device, platform, or application before trusting it with sensitive operations or data. The core idea is that a component, typically a Trusted Platform Module (TPM) or a Trusted Execution Environment (TEE) (like Intel SGX or ARM TrustZone), generates a cryptographically signed report called a quote or attestation report, which describes the software and hardware state (e.g., firmware, OS, application hashes). The attestation process begins with the platform generating measurement values—secure hashes of software components—during the boot or initialization process. These are stored in Platform Configuration Registers (PCRs) in a TPM or used by a TEE enclave. When a remote verifier (e.g., a server or controller) requests attestation, the device signs these measurements using an Attestation Identity Key (AIK) or enclave signing key. The signed report is then sent to the verifier, who checks that it was produced by genuine hardware (using certificates from a manufacturer or trusted CA), and compares the reported values against a known-good baseline. In practice, attestation is used in zero-trust architectures, IoT device onboarding, confidential computing workflows, and secure boot processes. Implementing it involves integrating support for TPM commands or TEE SDK APIs, securely managing identity certificates, and maintaining a trusted registry of valid configurations. Remote attestation can be enhanced using protocols like EPID, DCAP, or RA-TLS, and should include protections against replay attacks, key misuse, and spoofed attestations. Ultimately, attestation builds trust in otherwise untrusted environments by proving that a device or application is in a known and secure state before critical operations are allowed.")
        stuff = True
    if use_case == "I want to audit or verify system/data integrity" or not use_case or more:
        expander_9 = st.expander("Cryptographic Hashes")
        expander_9.write("To best use cryptographic hashes, you start by identifying data that needs integrity protection, such as passwords, files, messages, or transactions. A cryptographic hash function—like SHA-256, SHA-3, or BLAKE3—is then used to generate a fixed-length, unique hash (digest) from this data, which acts like a digital fingerprint. Technically, hashes are used in various ways: to store passwords securely (usually with salts and a slow hash function like bcrypt or Argon2), to verify file or message integrity (by comparing stored and recalculated hashes), or to digitally sign data (where the hash is signed instead of the raw message for efficiency). In implementation, it’s critical to use secure, collision-resistant hash functions and avoid outdated ones like MD5 or SHA-1. For high-security applications, hashing should be combined with additional techniques like HMAC (for message authentication) or Merkle trees (for verifying data structures efficiently). Hashes must also be stored or transmitted securely to avoid substitution attacks, ensuring that integrity and authenticity checks are meaningful in the system’s broader security model.")
        stuff = True
    if (privacy <= 2 and synth) or not use_case or more:
        expander_10 = st.expander("Synthetic Data")
        expander_10.write("In applying synthetic data, you start by identifying the real datasets that need to be protected—usually ones containing sensitive or personally identifiable information (PII)—and selecting the right generation method based on the data type and use case. Synthetic data can be created using statistical models, generative machine learning models like GANs or VAEs, or rule-based simulators that mimic the structure and statistical properties of real data without revealing any actual records. Technically, this involves training a model on the original dataset, ensuring it captures relevant distributions and correlations, and then sampling from the model to produce synthetic records. To enhance privacy, techniques such as differential privacy can be integrated into the generation process to prevent leakage of individual-level information. The resulting synthetic data can be used for development, testing, or sharing with third parties without exposing real user data. Implementation also requires validation: synthetic datasets must be evaluated for utility (how well they preserve patterns) and privacy risk (how dissimilar they are from the original data). It's crucial to maintain metadata, enforce governance policies, and ensure synthetic data is not mistakenly treated as real data in downstream workflows.")
        stuff = True
    if (reversible >= 3 and use_case == "I want to audit or verify system/data integrity") or (reversible >= 2 and use_case == "I want my system to be verifiable/trusted by another party") or not use_case or more:
        expander_11 = st.expander("Blockchain")
        expander_11.write("With Blockchain, you begin by defining the use case—such as secure data logging, digital asset management, smart contracts, or decentralized identity—and selecting an appropriate blockchain platform like Ethereum, Hyperledger Fabric, or Solana, based on your requirements for decentralization, scalability, and consensus. A blockchain works by organizing data into blocks, each cryptographically linked to the previous one using hash functions, creating an immutable, tamper-evident ledger. Technically, you deploy nodes (servers) that maintain a synchronized copy of the ledger and participate in a consensus protocol (e.g., Proof of Work, Proof of Stake, or PBFT) to validate transactions and add new blocks. Data is recorded as transactions, signed by private keys to prove authenticity, and broadcast across the network. For permissioned blockchains, you must manage identities and access control through membership services. Smart contracts—programs that execute automatically on the blockchain—are used to encode business logic in a decentralized, transparent way. Implementation also involves setting up APIs or SDKs for application integration, managing on-chain/off-chain data interactions, and securing keys and wallets used for signing. Finally, ongoing considerations include network governance, scalability, gas or transaction fees, data privacy (e.g., through zk-SNARKs or sidechains), and compliance with legal standards depending on the domain.")
        stuff = True
    if (use_case == "I am conducting analysis on data (locally or centrally)" and malicious >= 3 and trust <= 2) or not use_case or more:
        expander_12 = st.expander("Federated Learning")
        expander_12.write("For Federated Learning, you start by designing a machine learning architecture where model training occurs across decentralized client devices—like smartphones, IoT devices, or enterprise endpoints—without ever collecting their raw data. Instead, each client downloads a global model, trains it locally on its own private data, and sends only the model updates (gradients or weights) back to a central server. These updates are then aggregated—typically using algorithms like Federated Averaging (FedAvg)—to update the global model. To implement this, you use FL frameworks such as TensorFlow Federated, PySyft, or Flower, which help coordinate training rounds, handle client heterogeneity, and manage communication. Security and privacy are critical, so techniques like Secure Aggregation (to prevent the server from seeing individual updates), Differential Privacy (to limit leakage through gradients), and robust aggregation (to resist malicious updates) are often applied. Implementation also requires a reliable client-server communication layer, client selection logic, and fallback mechanisms to handle partial participation or network failures. Federated Learning is ideal for applications like predictive text, healthcare analytics, or IoT intelligence—where data is siloed and privacy must be preserved—while still enabling collaborative model improvement across users or organizations.")
        stuff = True
    if not stuff:
        expander_13 = st.expander("Local Differential Privacy")
        expander_13.write("Implementing Local Differential Privacy (LDP) technically, requires first identifying the data collection points (e.g., client devices or browsers) and applying noise to the data before it leaves the user’s device. This typically involves integrating an LDP mechanism—such as randomized response for binary or categorical data, or local hashing schemes like RAPPOR or Optimized Unary Encoding for larger domains—into the client-side codebase. For numeric data, you might use Laplace noise scaled according to the chosen privacy budget. A critical technical consideration is selecting an appropriate epsilon (ε), which controls the balance between privacy and data utility. Smaller ε values (e.g., <0.5) provide stronger privacy but introduce more noise, making aggregate analysis less precise, while higher values (e.g., 1–3) yield better utility but weaken privacy guarantees. Epsilon should be chosen based on the sensitivity of the data, the frequency of data collection, and the acceptable risk level, often informed by academic norms (e.g., ε ≈ 1 is common in deployed systems). It’s also essential to implement mechanisms like per-user query limits, memoization (to ensure the same input always results in the same noisy output), and cumulative privacy accounting to control total privacy loss over time. Data collected with LDP must be aggregated using statistical post-processing techniques (e.g., expectation-maximization or Bayesian denoising) to recover meaningful insights while respecting the privacy guarantees set by ε.")