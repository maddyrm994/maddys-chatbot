import streamlit as st
from groq import Groq

# --- Page Configuration ---
st.set_page_config(
    page_title="Maddy's Chatbot",
    page_icon="💬",
    layout="centered",
)

# --- App Title ---
st.title("💬 Maddy's Chatbot")

# --- Groq API Key Management ---
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = ""

def set_api_key(api_key):
    st.session_state.groq_api_key = api_key

# --- System Prompt ---
SYSTEM_PROMPT = "You are a digital version of Maddy. You are a friendly and helpful chatbot."

# --- UI for API Key Input ---
if not st.session_state.groq_api_key:
    st.subheader("Enter Your Groq API Key")
    st.markdown("To get your API key, visit [https://console.groq.com/keys](https://console.groq.com/keys)")
    
    groq_api_key_input = st.text_input("Groq API Key", type="password")
    
    if st.button("Submit"):
        if groq_api_key_input:
            set_api_key(groq_api_key_input)
            st.rerun()
        else:
            st.error("Please enter a valid API key.")
else:
    # --- Chat Interface ---
    st.caption("A blazing fast chatbot for friendly chat purposes")

    # --- Initialize Groq Client and Set Model ---
    try:
        client = Groq(api_key=st.session_state.groq_api_key)
        MODEL_ID = "llama3-70b-8192"
    except Exception as e:
        st.error(f"Failed to initialize Groq client: {e}")
        st.stop()

    # --- Chat History Management ---
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # --- Helper Function to Clear Chat ---
    def clear_chat_history():
        """Clears the chat history stored in the session state."""
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # --- UI Elements for Chat Management ---
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button('Clear Chat'):
            clear_chat_history()
            st.rerun()

    # --- Display Chat History ---
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # --- Chat Input and Response Generation ---
    if prompt := st.chat_input("Ask anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                with st.spinner("I am thinking..."):
                    chat_completion = client.chat.completions.create(
                        messages=st.session_state.messages,
                        model=MODEL_ID,
                    )
                    response = chat_completion.choices[0].message.content
                    st.markdown(response)
                    
                    st.session_state.messages.append({"role": "assistant", "content": response})

            except Exception as e:
                st.error(f"An error occurred: {e}", icon="🚨")
