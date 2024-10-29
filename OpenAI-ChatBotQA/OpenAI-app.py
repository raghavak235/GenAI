import os

import openai
import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

#  LANGSMITH  TRACKING
os.environ['LANGCHAIN_API_KEY']=os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACKING_V2']="true"
os.environ['LANGCHAIN_PROJECT']="QA ChatBot With OPENAI"

#  PROMPT TEMPLATE
prompt = ChatPromptTemplate.from_messages(
    [
        ('system','you are a helpful assistant. Please response to the user queries'),
        ('user', 'Question:{question}')
    ]
)

def generate_response(question, api_key, llm, temperature, max_tokens):
    openai.api_key=api_key
    llm=ChatOpenAI(models=llm)
    output_parser=StrOutputParser()
    chain = prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer

# Title of the app
st.title('Enhanced Q&A ChatBot With OpenAI')

# Sidebar for settings
st.sidebar.title('Settngs')
api_key=st.sidebar.text_input("Enter your OPEN API Key:", type="password")

# Drop Down to select the OpenAI models
llm=st.sidebar.selectbox('Select an Open AI Model', ['gpt-4o','gpt-4-turbo','gpt-4'])

#  Adjust response parameter
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider('Max Tokens', min_value=50, max_value=300,value=150)

#  Main Interface for user input

st.write('Go ahead and ask any questions')
user_input=st.text_input('You:')

if user_input:
    response = generate_response(user_input, api_key, llm, temperature, max_tokens)
    st.write(response)
else:
    st.write('Please provide the query')