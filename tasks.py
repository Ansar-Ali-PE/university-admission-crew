from crewai import Task

def create_tasks(scanner, matchmaker, ranker, advisor):
    task1 = Task(
        description=(
            "Analyze the following student profile:\n{student_profile}\n\n"
            "Assess core eligibility metrics like GPA, test scores, and coursework."
        ),
        expected_output="A structured summary identifying academic strengths and initial baseline eligibility.",
        agent=scanner
    )

    task2 = Task(
        description=(
            "Based on the student's profile and the eligibility assessment, "
            "identify 4-5 optimal majors or degree pathways matching their interests and career goals."
        ),
        expected_output="A list of matching academic programs with structural reasons why they align with the student.",
        agent=matchmaker
    )

    task3 = Task(
        description=(
            "Take the matched programs and split them into strategic tiers: Reach, Target, and Safety. "
            "Provide brief tactical arguments for why each program falls into its specific bucket."
        ),
        expected_output="A tiered, prioritized categorization of the selected programs.",
        agent=ranker
    )

    task4 = Task(
        description=(
            "Compile the complete University Admission Evaluation Report. "
            "Include a supportive introductory summary, the tiered list, and clear operational next steps."
        ),
        expected_output="A professional, comprehensive markdown report designed for the student.",
        agent=advisor
    )

    return [task1, task2, task3, task4]
