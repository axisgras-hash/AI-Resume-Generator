# import streamlit as st
# # streamlit: Web based app making
# # lite python framework

# st.title("AI Resume Maker")

# st.markdown("""## User can create or
# download AI created Resume based on high ATS
# Score""")


# #==================AGENT CODE===================
# # Step 2: Load Modules

# import os
# import time
# import langchain
# from langchain.agents import create_agent
# from langchain_groq import ChatGroq
# from langchain_google_genai import ChatGoogleGenerativeAI
# import pytesseract as pyt
# from tavily import TavilyClient
# from langchain.messages import SystemMessage, HumanMessage
# import numpy as np
# import streamlit as st
# from langchain_community.document_loaders import PyMuPDFLoader


# # ================API KEY LOAD===================

# GOOGLE_API_KEY = st.sidebar.text_input("GOOGLE_API_KEY",type="password")
# GROQ_API_KEY = st.sidebar.text_input("GROQ_API_KEY",type="password")
# TAVILY_API_KEY = st.sidebar.text_input("TAVILY_API_KEY",type="password")


# # ===============MODEL BUILDING=============
# model = ChatGoogleGenerativeAI(
#     model = 'gemini-3.5-flash-lite',
#     google_api_key = GOOGLE_API_KEY
# )

# # tool
# def search_recent_news_jobs(query):
#   """This function helps to search
#   recent news or recent jobs
#   related to given search query
#   suppose user write Python Developer jobs
#   It should return trending news and jobs link"""
#   client = TavilyClient(
#       api_key = TAVILY_API_KEY
#       )
#   return client.search(query)



# # agent creation
# from langchain.agents import create_agent

# agent = create_agent(
#     model = model,
#     tools = [search_recent_news_jobs]
# )


# # ==== PROMPT GENERATOR================
# def prompt_generator(agent = agent):
#   """This function help to give detailed prompt
#   followed by Chain of thoughts and
#   persona based prompting, main task is to give
#   detailed prompt to build Resume for
#   Students or Experienced person
#   Based on their given personal information.
#   """

#   prompt = """You are a senior HR resume analyzer,
#   main task is to give
#   detailed prompt to build Resume for
#   Students or Experienced person
#   Based on their given personal information.
#   System Instruction I want Model to generate resume
#   in HTML format , include that in prompt"""

#   response = agent.invoke(prompt)
#   file_name = 'prompt.py'
#   with open(file_name, 'w') as f:
#     f.write(response.content[-1]['text'])
#   return "Prompt file generated Successfully, agent can read it"

# prompt_generator(model)
# # tool 2:
# def resume_maker_prompt():
#   """This function just gives
#   updated prompt for model"""

#   with open('prompt.py', 'r') as f:
#     prompt = f.read()
#   return prompt

# # ===========GENERATE RESUME========
# prompt = """You are a helpful AI assistant
# with job resume maker, your task is to give
# HTML format resume, with proper designing using recent CSS and JS
# code, with professional design Format.
# User will upload data and return HTML format resume
# always use different color or styling"""

# final_prompt = prompt + resume_maker_prompt()

# user_details = """user details: given below:
# Give Python Developer Resume"""

# query = final_prompt + user_details

# if st.button("Generate Resume"):
#   with st.spinner("Running Agent...."):

#     response = agent.invoke({'messages':[{'role':'user','content':query}]})
#     code = response['messages'][-1].content[-1]['text']

#     #st.markdown(code)
#     st.html(code, width="stretch", unsafe_allow_javascript=True)



import streamlit as st
from tavily import TavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
import tempfile
from langchain_community.document_loaders import PyMuPDFLoader

st.set_page_config(
    page_title="AI Resume Maker",
    page_icon="🚀",
    layout="wide"
)

# ------------------- CSS --------------------

st.markdown("""
<style>

.main{
    background:#f7f9fc;
}

.hero{
padding:30px;
border-radius:20px;
background:linear-gradient(90deg,#4F46E5,#06B6D4);
color:white;
text-align:center;
margin-bottom:20px;
}

.card{
background:white;
padding:20px;
border-radius:15px;
box-shadow:0 5px 20px rgba(0,0,0,.15);
margin-bottom:15px;
}

.stButton>button{
width:100%;
background:#4F46E5;
color:white;
border-radius:10px;
height:50px;
font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------

st.markdown("""
<div class="hero">
<h1>🚀 AI Resume Builder</h1>
<h4>Create ATS Optimized Resume with AI</h4>
</div>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------

st.sidebar.title("🔑 API Keys")

GOOGLE_API_KEY = st.sidebar.text_input(
    "Google API",
    type="password"
)

TAVILY_API_KEY = st.sidebar.text_input(
    "Tavily API",
    type="password"
)

# ---------------- Model ----------------

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY
)

def search_jobs(query):

    client = TavilyClient(api_key=TAVILY_API_KEY)

    return client.search(query)

agent = create_agent(
    model=model,
    tools=[search_jobs]
)

# ---------------- Tabs ----------------

tab1,tab2,tab3=st.tabs(
[
"👤 Resume",
"📄 Preview",
"💼 Jobs"
]
)

# ==========================================
# TAB 1
# ==========================================

with tab1:

    col1,col2=st.columns(2)

    with col1:

        name=st.text_input("Full Name")

        email=st.text_input("Email")

        phone=st.text_input("Phone")

        location=st.text_input("Location")

        experience=st.slider(
            "Experience",
            0,
            20,
            1
        )

    with col2:

        role=st.text_input(
            "Target Role"
        )

        skills=st.text_area(
            "Skills"
        )

        education=st.text_area(
            "Education"
        )

        projects=st.text_area(
            "Projects"
        )

    uploaded=st.file_uploader(
        "Upload Existing Resume",
        type="pdf"
    )

    extracted_text=""

    if uploaded:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp:

            tmp.write(uploaded.read())

            loader=PyMuPDFLoader(tmp.name)

            docs=loader.load()

            extracted_text="\n".join(
                [d.page_content for d in docs]
            )

            st.success("Resume Loaded Successfully")

# ==========================================
# Generate Button
# ==========================================

    if st.button("🚀 Generate Resume"):

        prompt=f"""

Create a beautiful ATS optimized HTML Resume.

Candidate

Name:{name}

Email:{email}

Phone:{phone}

Location:{location}

Experience:{experience}

Role:{role}

Skills:
{skills}

Education:
{education}

Projects:
{projects}

Existing Resume:
{extracted_text}

Return ONLY HTML.
Use modern CSS.
Responsive.
Professional colors.
"""

        with st.spinner("Generating Resume..."):

            response=agent.invoke(
            {
            "messages":[
            {
            "role":"user",
            "content":prompt
            }
            ]
            })

            html=response["messages"][-1].content

            st.session_state["resume"]=html

# ==========================================
# Preview
# ==========================================

with tab2:

    if "resume" in st.session_state:

        st.success("Resume Generated")

        st.components.v1.html(
            st.session_state["resume"],
            height=900,
            scrolling=True
        )

        st.download_button(
            "📥 Download HTML",
            st.session_state["resume"],
            file_name="resume.html"
        )

# ==========================================
# Jobs
# ==========================================

with tab3:

    job=st.text_input(
        "Search Jobs"
    )

    if st.button("Search"):

        with st.spinner():

            jobs=search_jobs(job)

            st.json(jobs)


