import streamlit as st
import requests

st.title("Liar's Dice 🎲 (Hugging Face Edition)")
st.write(
    "This chatbot uses a Hugging Face model for conversation. "
    "To use this app, enter your Hugging Face API token. You can get one [here](https://huggingface.co/settings/tokens)."
)

# User input for Hugging Face token
hf_token = st.text_input("Hugging Face API Token", type="password")
model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"  # You can change this model

if not hf_token:
    st.info("Please add your Hugging Face API token to continue.", icon="🗝️")
else:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Format messages into a single prompt
        history = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages])
        payload = {
            "inputs": f"{history}\nAssistant:",
            "parameters": {"max_new_tokens": 200, "temperature": 0.7},
        }

        headers = {
            "Authorization": f"Bearer {hf_token}"
        }

        response = requests.post(
            f"https://api-inference.huggingface.co/models/{model_id}",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            bot_reply = response.json()[0]["generated_text"].split("Assistant:")[-1].strip()
        else:
            bot_reply = f"Error: {response.status_code} - {response.text}"

        with st.chat_message("assistant"):
            st.markdown(bot_reply)

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
