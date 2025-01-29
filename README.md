# Gen AI Career Consultant

## Overview
Gen AI Career Consultant is a Streamlit-based application that leverages the power of Llama-3.3-70b-versatile (via Groq API) to analyze resumes and portfolios against job postings scraped from websites. 
It helps candidates understand their suitability for a role and provides recommendations to improve their chances of securing a job.

## Features
- **Job Posting Extraction**: Scrapes job descriptions from a given URL.
- **Resume Analysis**: Evaluates a resume against the job description and provides feedback.
- **Portfolio Analysis**: Analyzes a candidate’s portfolio CSV and checks skills match with job requirements.
- **AI-Powered Suggestions**: Provides recommendations for skill improvement, experience emphasis, and relevant interview questions.

## Installation & Setup
### Prerequisites
- Python 3.8+
- `pip` package manager

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the project directory and add the following:
```
GROQ_API_KEY=your_groq_api_key
```

## Usage
Run the Streamlit application:
```bash
streamlit run app.py
```

### Inputs Required
1. **Website URL** – Enter the URL of the job posting.
2. **Resume Upload** – Upload a resume file (`.pdf` or `.docx`).
3. **Portfolio Upload (Optional)** – Upload a CSV file containing technology skills.

### Output
- **Suitability Assessment**: Determines if the candidate is fit for the job.
- **Improvement Suggestions**: Highlights skills and experience areas to focus on.
- **Recommended Topics**: Lists areas for further learning.
- **Sample Interview Questions**: Generates role-specific interview questions.

## File Structure
```
.
├── app.py               # Main Streamlit app
├── requirements.txt     # Required Python libraries
├── .env                 # API key storage
└── README.md            # This file
```

## Technologies Used
- **LangChain** (for AI-driven text processing)
- **Groq API** (Llama-3.3-70b-versatile model)
- **Streamlit** (UI framework)
- **PyPDF2 & docx** (Resume parsing)
- **pandas** (Portfolio CSV processing)
- **chromadb** (Vector database, future enhancements)

## Future Enhancements
- **Support for more resume formats**
- **More detailed AI-driven insights**
- **Integration with job platforms (LinkedIn, Indeed, etc.)**

