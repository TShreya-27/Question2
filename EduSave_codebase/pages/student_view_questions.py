import streamlit as st

st.title("Student: View Questions")

if 'current_exam' in st.session_state and 'exams' in st.session_state:
    exam_id = st.session_state.current_exam
    exam_details = st.session_state.exams.get(exam_id)
    if exam_details:
        st.header(f"Exam: {exam_details['title']}")
        for i, q in enumerate(exam_details['questions']):
            st.write(f"Q{i+1}: {q['question']}")
    else:
        st.warning("No exam details found.")
else:
    st.info("No exam selected. Please select an exam from the dashboard.")
