from crewai import Agent

def get_document_scanner(llm):
    return Agent(
        role="Document Scanner and Eligibility Specialist",
        goal="Accurately evaluate student transcripts, GPA, and test scores against competitive university thresholds.",
        backstory=(
            "You are a meticulous university admissions registrar. You screen profiles "
            "to check if basic academic baselines and prerequisites are satisfied."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def get_program_matchmaker(llm):
    return Agent(
        role="Program Matchmaking Expert",
        goal="Map a student's academic background, project history, and career goals to matching university majors.",
        backstory=(
            "You are an expert academic advisor. You excel at finding degrees and career paths "
            "where the student's background gives them a distinct competitive edge."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def get_priority_ranker(llm):
    return Agent(
        role="Strategic Priority Ranker",
        goal="Categorize matched programs into Reach, Target, and Safety tiers with clear justification.",
        backstory=(
            "You are an admission strategist. You assess historical competitiveness "
            "and rank user program options logically to optimize their admissions strategy."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def get_student_advisor(llm):
    return Agent(
        role="Lead Student Admissions Counselor",
        goal="Synthesize all findings into an empathetic, highly structured, and actionable report.",
        backstory=(
            "You are a veteran high school guidance counselor. You transform data tables "
            "and strategic breakdowns into an inspiring, step-by-step roadmap for the student."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
