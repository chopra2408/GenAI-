#import libraries
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
import pandas as pd
import chromadb
import uuid
import streamlit as st
import PyPDF2
import docx
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv
import os
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

#initialize model
llm = ChatGroq(
    temperature=0,
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)

#parse pdf
def parse_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

#parse docx
def parse_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

#extract resume info
def extract_resume_info(file):
    if file.type == "application/pdf":
        text = parse_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = parse_docx(file)
    else:
        return {"error": "Unsupported file format"}
    return {"content": text}

#preprocess
def preprocess_job_posting(url, portfolio_csv):
    loader = WebBaseLoader(url)
    page_data = loader.load().pop().page_content

    prompt_extract = PromptTemplate.from_template('''
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing
        the following keys: "role", "experience", "skills", and "description".
        Only return a valid JSON response.
        ### VALID JSON (NO PREAMBLE):
    ''')

    chain_extract = prompt_extract | llm | StrOutputParser()
    response = chain_extract.invoke({'page_data': page_data})

    json_parser = JsonOutputParser()
    json_res = json_parser.parse(response)

    return json_res

#resume analysis
def analyze_resume_for_job(resume_text, job_description):
    prompt_resume_analysis = PromptTemplate.from_template("""
        ### JOB DESCRIPTION:
        {job_description}

        ### RESUME CONTENT:
        {resume_text}

        ### INSTRUCTION:
        Based on the job description and the resume, analyze whether the candidate is suitable for the role. Consider the following factors:
        - Skills match
        - Experience and qualifications
        - Relevance of previous job roles

        Provide the following output:
        1. **Suitability**: A brief evaluation of whether the candidate is suitable for the role (Yes/No).
        2. **Suggestions**: A list of suggestions to improve the candidate's resume, including:
           - Skills to highlight
           - Experience to emphasize
           - Any other relevant advice
        3. **Suggested Topics**: List of deep topics to learn to further improve suitability for the job.
        4. **Interview Questions**: Based on the job description and topics, provide interview questions to assess suitability for the job.

        Only return valid JSON.
        ### VALID JSON (NO PREAMBLE):
    """)

    chain_resume_analysis = prompt_resume_analysis | llm | JsonOutputParser()
    response = chain_resume_analysis.invoke({
        "job_description": job_description,
        "resume_text": resume_text
    })
    return response

#portfolio analysis
def analyze_portfolio_for_job(portfolio_csv, job_description):
    df = pd.read_csv(portfolio_csv)
    portfolio_skills = df['Technology'].tolist()

    prompt_portfolio_analysis = PromptTemplate.from_template("""
        ### JOB DESCRIPTION:
        {job_description}

        ### PORTFOLIO SKILLS:
        {portfolio_skills}

        ### INSTRUCTION:
        Based on the job description and the portfolio skills, analyze whether the candidate is suitable for the role. Consider the following:
        - Skills match between portfolio and job description.
        - Suggest any skills or experience to add in the portfolio to improve the chances of getting the job.

        Provide the following output:
        1. **Suitability**: A brief evaluation of whether the candidate's portfolio is suitable for the job (Yes/No).
        2. **Suggestions**: A list of suggestions to improve the portfolio, including:
           - Skills to add
           - Experience to highlight
           - Any other relevant advice
        3. **Suggested Topics**: List of deep topics to learn to further improve suitability for the job.
        4. **Interview Questions**: Based on the job description and topics, provide interview questions to assess suitability for the job.

        Only return valid JSON.
        ### VALID JSON (NO PREAMBLE):
    """)

    chain_portfolio_analysis = prompt_portfolio_analysis | llm | JsonOutputParser()
    response = chain_portfolio_analysis.invoke({
        "job_description": job_description,
        "portfolio_skills": portfolio_skills
    })
    return response


def main(url, portfolio_csv, resume_input, use_resume=True):
    try:
        job_desc = preprocess_job_posting(url, portfolio_csv)
        
        if use_resume and resume_input:
            resume_info = extract_resume_info(resume_input)
            analysis_result = analyze_resume_for_job(resume_info["content"], job_desc)
        
        elif portfolio_input:
            analysis_result = analyze_portfolio_for_job(portfolio_csv, job_desc)
        
        else:
            raise ValueError("Please provide either a resume or portfolio.")

        return analysis_result
    except Exception as e:
        return {"error": str(e)}

st.title("Gen AI Career Consultant")
url_input = st.text_input(label="Website URL", placeholder="Enter the URL of the job posting:")
portfolio_input = st.file_uploader(label="Upload Portfolio CSV", type=["csv"])
resume_input = st.file_uploader(label="Upload Resume", type=["pdf", "docx"])

if st.button("Process"):
    if url_input and (portfolio_input or resume_input):
        result = main(url_input, portfolio_input, resume_input, use_resume=True)
        st.json(result)
    else:
        st.error("Please provide URL and either a Resume or Portfolio file.")

if __name__ == "__main__":
    main()