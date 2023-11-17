import streamlit as st
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader, BSHTMLLoader
import requests
from bs4 import BeautifulSoup

load_dotenv()

llm = ChatOpenAI(temperature=.7, model="gpt-3.5-turbo-16k")

template = """You are Mark Barshay. Given the resume and job description, write a cover letter from yourself explaining why you, the candidate, is uniquely qualified for the job. Cite specific instances from the resume.  The tone should be {tone} and the length should be {length}.
Resume: {resume}
Job Description: {job_description}
Cover Letter:"""
prompt_template = PromptTemplate(input_variables=["resume", "job_description", "tone", "length"], template=template)
cover_letter_chain = LLMChain(llm=llm, prompt=prompt_template)

st.title('💪Mark Barshay Cover Letter Generator💪')

st.sidebar.title('Upload your resume')

def load_resume():
    file_path = "./MB_Resume.pdf"
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    resume = ' '.join([page.page_content for page in pages])
    st.sidebar.text('Loaded file: ' + file_path)
    return resume

resume = load_resume()

st.sidebar.title('Enter Job Description')
# job_description_option = st.sidebar.radio('Choose an option', ['URL', 'Text'])

job_description = st.sidebar.text_area('Paste the Job Description')

st.sidebar.title('Choose Tone and Length')
tone = st.sidebar.selectbox('Tone', ['Staten Island Guido','Professional' ])
length = st.sidebar.selectbox('Length', ['Short','Long' ])

if st.sidebar.button('Generate Cover Letter'):
    with st.spinner(text="I'm thinkin' ova here..."):
        cover_letter = cover_letter_chain.run({"resume": resume, "job_description": job_description, "tone": tone, "length": length})
    st.write(cover_letter)


