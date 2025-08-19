import streamlit as st
from groq import Groq

# --- Page Configuration ---
st.set_page_config(
    page_title="Maddy's Chatbot",
    page_icon="💬",
    layout="centered",
)

# --- App Title and Description ---
st.title("💬 Maddy's Chatbot")
st.caption("A blazing fast chatbot for friendly chat purposes")

# --- Groq API Key Configuration ---
# All secrets are still managed in .streamlit/secrets.toml
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("GROQ_API_KEY not found in Streamlit secrets. Please add it.")
    st.stop()

# --- Initialize Groq Client and Set Model ---
client = Groq(api_key=groq_api_key)
# The model is now hardcoded
MODEL_ID = "llama3-70b-8192"


# --- Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Helper Function to Clear Chat ---
def clear_chat_history():
    """Clears the chat history stored in the session state."""
    st.session_state.messages = []

# Place the "Clear Chat" button at the top, next to the caption
# Using columns to place it on the right side for better UI
col1, col2 = st.columns([3, 1]) # Adjust ratio as needed
with col2:
    if st.button('Clear Chat'):
        clear_chat_history()
        st.rerun() # Rerun the app to reflect the change immediately

# --- Display Chat History ---
# Loop through the messages stored in the session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input and Response Generation ---
if prompt := st.chat_input("Ask anything..."):
    # Add user's message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display the assistant's response
    with st.chat_message("assistant"):
        try:
            with st.spinner("I am thinking..."):
                chat_completion = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model=MODEL_ID, # Use the hardcoded model ID
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                
                # Add assistant's response to history
                st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"An error occurred: {e}", icon="🚨")
