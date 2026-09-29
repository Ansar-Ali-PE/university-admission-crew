__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Keep everything else below it exactly as it was:
import streamlit as st
from langchain_groq import ChatGroq
from crewai import Crew, Process
...

import streamlit as st
from langchain_groq import ChatGroq
from crewai import Crew, Process

# Import modular configurations
from agents import (
    get_document_scanner,
    get_program_matchmaker,
    get_priority_ranker,
    get_student_advisor
)
from tasks import create_tasks

# Page configuration
st.set_page_config(page_title="UniAdmit AI", page_icon="🎓", layout="wide")

st.title("🎓 Multi-Agent University Admission Advisor")
st.subheader("Powered by CrewAI & Groq")

# Sidebar for API configurations
st.sidebar.header("Configuration")
groq_api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
model_choice = st.sidebar.selectbox("Select Groq Model:", ["llama3-70b-8192", "mixtral-8x7b-32768"])

# Layout setup
col1, col2 = st.columns()

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
                    # Initialize LLM via Groq
                    llm = ChatGroq(
                        groq_api_key=groq_api_key,
                        model_name=model_choice,
                        temperature=0.3
                    )
                    
                    # Instantiate Agents
                    scanner = get_document_scanner(llm)
                    matchmaker = get_program_matchmaker(llm)
                    ranker = get_priority_ranker(llm)
                    advisor = get_student_advisor(llm)
                    
                    # Create Tasks
                    tasks = create_tasks(scanner, matchmaker, ranker, advisor)
                    
                    # Structure the raw profile text input
                    profile_payload = f"""
                    Name: {name}
                    GPA: {gpa}
                    Test Scores: {test_scores}
                    Coursework: {coursework}
                    Interests: {interests}
                    Career Goals: {goals}
                    """
                    
                    # Initialize Crew
                    crew = Crew(
                        agents=[scanner, matchmaker, ranker, advisor],
                        tasks=tasks,
                        process=Process.sequential,
                        verbose=True
                    )
                    
                    # Execute crew workflow
                    result = crew.kickoff(inputs={"student_profile": profile_payload})
                    
                    # Display output
                    st.success("Analysis Complete!")
                    st.markdown(result.raw)
                    
                except Exception as e:
                    st.error(f"An error occurred during workflow execution: {e}")
