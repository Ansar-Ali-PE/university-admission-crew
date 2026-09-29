# 1. High-priority system patch for SQLite (Must be at the absolute top of the file)
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# 2. Initialize Streamlit & Page Configuration immediately after the patch
import streamlit as st
st.set_page_config(page_title="UniAdmit AI", page_icon="🎓", layout="wide")

# 3. Import remaining heavy orchestration packages
import os
from langchain_groq import ChatGroq
from crewai import Crew, Process

# 4. Import modular configurations from your repository files
from agents import (
    get_document_scanner,
    get_program_matchmaker,
    get_priority_ranker,
    get_student_advisor
)
from tasks import create_tasks

# 5. Render App Header UI
st.title("🎓 Multi-Agent University Admission Advisor")
st.subheader("Powered by CrewAI & Groq")

# 6. Sidebar Configuration Menu (Updated with active Groq production models)
st.sidebar.header("Configuration")
groq_api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
model_choice = st.sidebar.selectbox(
    "Select Groq Model:", 
    ["groq/llama-3.3-70b-versatile", "groq/llama-3.1-8b-instant"]
)

# 7. Form Layout Setup (Explicitly passing integer 2)
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Enter Student Details")
    name = st.text_input("Full Name", "Alex Chen")
    gpa = st.text_input("GPA (e.g., 3.65/4.0)", "3.65 / 4.0")
    test_scores = st.text_input("Standardized Test Scores (SAT/ACT/GRE)", "SAT: 1420 (M: 740, R: 680)")
    coursework = st.text_area("Key Coursework / AP Classes", "AP Calculus BC (A), AP Physics (B+), AP English (A-)")
    interests = st.text_area("Core Interests & Projects", "Building basic robotics kits, coding Python games, climate change apps")
    goals = st.text_input("Career Goals", "Software Engineering or Data Science in climate tech")

with col2:
    st.markdown("### 📋 Evaluation Report")
    
    if st.button("Generate Strategic Recommendation", type="primary"):
        if not groq_api_key:
            st.error("Please enter your Groq API Key in the sidebar to proceed.")
        else:
            with st.spinner("Agents are analyzing profile data, matching programs, and ranking priorities..."):
                try:
                    # Inject the key into the environment so CrewAI's litellm layer can authenticate
                    os.environ["GROQ_API_KEY"] = groq_api_key
                    
                    # Initialize LLM via Groq wrapper
                    llm = ChatGroq(
                        groq_api_key=groq_api_key,
                        model_name=model_choice,
                        temperature=0.3
                    )
                    
                    # Instantiate Modular Agents
                    scanner = get_document_scanner(llm)
                    matchmaker = get_program_matchmaker(llm)
                    ranker = get_priority_ranker(llm)
                    advisor = get_student_advisor(llm)
                    
                    # Create Sequential Tasks Pipeline
                    tasks = create_tasks(scanner, matchmaker, ranker, advisor)
                    
                    # Package the student data payload structured string
                    profile_payload = f"""
                    Name: {name}
                    GPA: {gpa}
                    Test Scores: {test_scores}
                    Coursework: {coursework}
                    Interests: {interests}
                    Career Goals: {goals}
                    """
                    
                    # Initialize multi-agent Execution Crew
                    crew = Crew(
                        agents=[scanner, matchmaker, ranker, advisor],
                        tasks=tasks,
                        process=Process.sequential,
                        verbose=True
                    )
                    
                    # Execute agents pipeline workflow
                    result = crew.kickoff(inputs={"student_profile": profile_payload})
                    
                    # Safely render markdown extraction text string output from the crew object
                    st.success("Analysis Complete!")
                    st.markdown(result.raw)
                    
                except Exception as e:
                    st.error(f"An error occurred during workflow execution: {e}")
