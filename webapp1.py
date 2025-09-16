import streamlit as st
from pdfextractor import text_extractor
import google.generativeai as genai
import os

key  = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key = key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

resume_text = job_desc = None

#Upload Resume
st.sidebar.title(':red[Upload Your Resume [PDF Only]]')
file = st.sidebar.file_uploader('Resume', type=['PDF'])
if file:
    resume_text = text_extractor(file)
    

#Lets Define the Main Page

st.title(':red[SKILLMATCH] - Ai Assisted Skill Matching Tool')
st.markdown('#### This application will match your resume and the job description. It will create a detailed report on the match')

tips = '''Follow these steps to proceed:
* Upload your updated resume in the sidebar. (PDF only)
* Copy and Paste the job description below for which you are applying.
* Click the button and see the match.'''

st.write(tips)

job_desc = st.text_area('Copy and Paste the Job Description here. [Press Ctrl + Enter]', max_chars=10000)

prompt = f'''Assume you are an expert in skill matching and creating profile.
Match the following resume with the job description provided by the user.

resume = {resume_text}
job description = {job_desc}

your output should follow as
* Give a brief description of the applicant in 3 to 5 lines.
* Give a range expected ATS score along the the matching and non matching keyword.
* Give the chances  of getting shortlisted for the position in percentage.
* Perform SWOT analysis and discuss each everything in bullet points.
* Suggest what all improvement can be made on the resume uploaded by the user in order to get better ATS and increase in percentage of getting shortlisted.
* Also create two customised resume as per the the job description provides to get better ATS and increase in percentage of getting shortlisted.
* Use bullet points and tables wherever required.'''

if job_desc:
    if resume_text:
        response = model.generate_content(prompt)
        st.write(response.text)
    else: 
        st.write('Please upload the resume')