import os

import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses Google's Gemini model to generate responses. "
    "The Gemini API key is read from `.streamlit/secrets.toml` (you can get a key [here](https://aistudio.google.com/app/apikey)). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Resolve the Gemini API key in this order:
#   1. .streamlit/secrets.toml (local) / App settings > Secrets (Streamlit Community Cloud)
#   2. GEMINI_API_KEY environment variable
#   3. Manual input in the sidebar (fallback)
def get_api_key() -> str:
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        key = ""
    if not key:
        key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        key = st.sidebar.text_input("Gemini API Key", type="password")
    return (key or "").strip()


gemini_api_key = get_api_key()
if not gemini_api_key:
    st.info(
        "Gemini API key not found. Add it to `.streamlit/secrets.toml` "
        "(or the Secrets panel on Streamlit Community Cloud), "
        "or enter it in the sidebar.",
        icon="🗝️",
    )
else:

    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-3.8-flash")

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Convert chat history for Gemini API.
        gemini_messages = [
            {
                "role": "user" if m["role"] == "user" else "model",
                "parts": [m["content"]],
            }
            for m in st.session_state.messages
        ]

        # Generate a response using the Gemini API.
        try:
            stream = model.generate_content(gemini_messages, stream=True)

            def stream_generator():
                for chunk in stream:
                    if chunk.text:
                        yield chunk.text

            # Stream the response to the chat using `st.write_stream`, then store it in 
            # session state.
            with st.chat_message("assistant"):
                response = st.write_stream(stream_generator)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error generating response (gemini-3.8-flash): {e}")
            st.info(
                "If you receive a 404 (NotFound) error, please check:\n"
                "1. Your API key was obtained from Google AI Studio (https://aistudio.google.com/app/apikey).\n"
                "2. Ensure your account has access to the gemini-3.8-flash model."
            )
