import streamlit as st
import google.generativeai as genai
from langchain_core.messages import AIMessage, HumanMessage

api_key = "#########Your API KEY###########"
genai.configure(api_key=api_key)

st.title("Conversational ChatBot Using Gemini AI")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content =  "Hi there, How can i help You?"),
    ]

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)


# for m in genai.list_models():
#   if "generateContent" in m.supported_generation_methods:
#     print(m.name)

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history = [])

user_query = st.chat_input("Write your message...")



if user_query is not None and user_query.strip() != "":
    response = chat.send_message(user_query)
    with st.chat_message("Human"):
        st.markdown(user_query)
    with st.chat_message("AI"):
        st.markdown(response.text)
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    st.session_state.chat_history.append(AIMessage(content = response.text))
