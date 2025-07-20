import streamlit as st
from groq import Groq

st.set_page_config(page_title="Career Counselor AI", page_icon="🎓")

st.title("🎓 Career Guidance Chatbot")
st.markdown("Talk to your multilingual, human-like career mentor.")

groq_client = Groq(api_key=st.secrets.get("GROQ_API_KEY") or "your-groq-api-key")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a warm, multilingual, human-like career counsellor. "
                "Greet the user empathetically. Accept free-flowing, mixed-language inputs. "
                "Ask thoughtful questions, guide them step-by-step, and act like a real human mentor."
            )
        }
    ]

# Display previous messages (Streamlit's new chat format)
for msg in st.session_state.messages[1:]:  # Skip system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        chat_completion = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=1024
        )
        reply = chat_completion.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
