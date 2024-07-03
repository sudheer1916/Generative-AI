import streamlit as st
import langchain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAI

st.title("Ask Question to Database using LLM")
query_question = st.text_input("Ask a Question...")

template = '''
Based on the table schema below, write a sql query that would answer the user's question: {schema}
Question: {question}
SQL query
'''
prompt = ChatPromptTemplate.from_template(template)
prompt.format(schema="my schema", question = "how many user are there?")

db_user = "your_username"
db_password = "your_password"
db_host = "your_hostname"
db_name = "your_database_name"
db_uri = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"
# db_uri = "mysql+mysqlconnector://root:root@localhost:3306/atliq_tshirts"
db = SQLDatabase.from_uri(db_uri)

def get_schema(_):
    return db.get_table_info()

api_key = "##########YOUR API KEY###############"
llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key)
# llm = genai.GenerativeModel('gemini-1.5-flash')


sql_chain = (
    RunnablePassthrough.assign(schema = get_schema)
    | prompt
    | llm.bind(stop = "\nSQL Result:")
    | StrOutputParser()
)
# sql_chain.invoke({"question" : "how many small tshirts are there?"})

#==================================================================================================================

# main code 

template = '''
Based on the table schema below, question, sql query and sql response, write a natural language response:
{schema}

Question : {question}
Sql Query : {query}
SQL Response : {response}

'''
prompt = ChatPromptTemplate.from_template(template)

def run_query(query):
    return db.run(query)

full_chain =(
    RunnablePassthrough.assign(query = sql_chain).assign(
        schema = get_schema,
        response = lambda var: run_query(var['query'])
    )
    | prompt
    | llm
)

button = st.button("Search")
if button:
    res = full_chain.invoke({'question' : query_question})
    st.header(res)
# full_chain.invoke({'question' : "How many medium blue tshirts are there?"})



