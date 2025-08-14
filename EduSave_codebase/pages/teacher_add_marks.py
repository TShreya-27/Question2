import streamlit as st
import pandas as pd

st.title("Teacher: Add Marks")

if 'exams' in st.session_state and st.session_state.exams:
    exam_ids = list(st.session_state.exams.keys())
    selected_exam = st.selectbox("Select Exam", exam_ids)
    exam_details = st.session_state.exams[selected_exam]
    st.header(f"Exam: {exam_details['title']}")
    submissions = st.session_state.submissions.get(selected_exam, {})
    if submissions:
        marks_data = []
        for student, sub in submissions.items():
            answers = sub['answers']
            student_marks = []
            st.subheader(f"Student: {student}")
            for i, ans in enumerate(answers):
                mark = st.number_input(f"Q{i+1} Mark for {student}", min_value=0, max_value=10, key=f"{student}_{selected_exam}_q{i}")
                student_marks.append(mark)
            total = sum(student_marks)
            marks_data.append({"Student": student, "Total Marks": total})
        st.write("Summary of Marks:")
        st.table(pd.DataFrame(marks_data))
    else:
        st.info("No submissions for this exam.")
else:
    st.info("No exams available.")
