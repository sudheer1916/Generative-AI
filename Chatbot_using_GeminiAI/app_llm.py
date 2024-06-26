import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import GoogleGenerativeAI
#from langchain_google_genai import ChatGoogleGenerativeAI


st.title("ChatBot Using Gemini AI")

if "chat_history" not in st.session_state:
  st.session_state.chat_history = [
    AIMessage(content =  "Hi there, How can i help You?"),
  ]

for message in st.session_state.chat_history:
  if isinstance(message, AIMessage):
    with st.chat_message("AI"):
      st.markdown(message.content)
  elif isinstance(message, HumanMessage):
    with st.chat_message("Human")
      st.markdown(message.content)

api_key = "AIzaSyCpoEPjRXaVIEgJvVpHszDAhFIdmPDsz64"
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
# llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)

# result = llm.invoke("Write a poem about AI")
# print(result.content)

user_query = st.chat_input("Wrie you message...")

response = llm.invoke(str(user_query))

if user_query is not None and user_query.strip() != "":
  with st.chat_message("Human"):
    st.markdown(user_query)
  with st.chat_message("AI"):
    st.markdown(response)
  st.session_state.chat_history.append(HumanMessage(content=user_query))
  st.session_state.chat_history.append(AIMessage(content = response))
