import streamlit as st
import pandas as pd
import json
import os
import random

# --- User Data Backend ---
USER_DB_FILE = "users_db.json"

def load_users():
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "r") as f:
            return json.load(f)
    else:
        # Default users
        return {
            "admin": {"password": "adminpassword", "role": "Admin"},
            "teacher1": {"password": "teacherpass", "role": "Teacher"},
            "student1": {"password": "studentpass", "role": "Student"}
        }

def save_users(users):
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f)

users_db = load_users()

# --- Session State Initialization ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'question_bank' not in st.session_state:
    st.session_state.question_bank = {
        "Physics": [
            {"question": "What is the formula for force?", "type": "Short Answer", "difficulty": "Easy"},
            {"question": "Explain Newton's First Law of Motion.", "type": "Long Answer", "difficulty": "Medium"}
        ],
        "History": [
            {"question": "Who was the first President of the United States?", "type": "MCQ", "options": ["Abraham Lincoln", "George Washington", "Thomas Jefferson"], "answer": "George Washington", "difficulty": "Easy"}
        ]
    }
if 'exams' not in st.session_state:
    st.session_state.exams = {}
if 'submissions' not in st.session_state:
    st.session_state.submissions = {}

# --- Initial Setup & Dummy Database ---
def initialize_state():
    """Initializes session state variables."""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'question_bank' not in st.session_state:
        st.session_state.question_bank = {
            "Physics": [
                {"question": "What is the formula for force?", "type": "Short Answer", "difficulty": "Easy"},
                {"question": "Explain Newton's First Law of Motion.", "type": "Long Answer", "difficulty": "Medium"}
            ],
            "History": [
                {"question": "Who was the first President of the United States?", "type": "MCQ", "options": ["Abraham Lincoln", "George Washington", "Thomas Jefferson"], "answer": "George Washington", "difficulty": "Easy"}
            ]
        }
    if 'exams' not in st.session_state:
        st.session_state.exams = {}
    if 'submissions' not in st.session_state:
        st.session_state.submissions = {}

# Dummy user database
users_db = {
    "admin": {"password": "adminpassword", "role": "Admin"},
    "teacher1": {"password": "teacherpass", "role": "Teacher"},
    "student1": {"password": "studentpass", "role": "Student"}
}

# --- AI Simulation ---
def generate_ai_question(topic, q_type, difficulty):
    """Simulates an AI model generating a question."""
    # In a real app, this would call a language model (e.g., GPT)
    return f"This is an AI-generated '{q_type}' question about '{topic}' with '{difficulty}' difficulty."

def generate_ai_exam_questions(subject, num_questions, difficulty):
    """Simulate AI generation of exam questions for a student."""
    # In a real app, this would call an AI model
    return [generate_ai_question(subject, "MCQ", difficulty) for _ in range(num_questions)]

# --- Authentication ---
def login_page():
    """Displays the login page and handles authentication."""
    st.header("Login to EduSave")
    login_role = st.radio("Select Login Type", ["Student", "Teacher"], key="login_role")
    username = st.text_input(f"{login_role} Username")
    password = st.text_input(f"{login_role} Password", type="password")
    login_attempted = st.button("Login")

    if login_attempted:
        users_db = load_users()  # Reload latest users
        if username in users_db and users_db[username]["password"] == password and users_db[username]["role"] == login_role:
            st.session_state.logged_in = True
            st.session_state.role = users_db[username]["role"]
            st.session_state.username = username
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error(f"Invalid {login_role} username or password")

    # Always show sign up option
    if st.button("New user? Sign up here"):
        st.session_state.show_register = True

    if st.session_state.get("show_register"):
        st.subheader("Sign Up - Register New User")
        reg_role = st.radio("Register as", ["Student", "Teacher"], key="reg_role_radio")
        new_username = st.text_input(f"{reg_role} Username", key="reg_username")
        new_password = st.text_input(f"{reg_role} Password", type="password", key="reg_password")
        if st.button("Register", key="reg_btn"):
            users_db = load_users()  # Reload latest users
            if new_username in users_db:
                st.error("Username already exists.")
            elif not new_username or not new_password:
                st.error("Please enter a username and password.")
            else:
                users_db[new_username] = {"password": new_password, "role": reg_role}
                save_users(users_db)
                st.success("Registration successful! You can now log in.")
                st.session_state.show_register = False

# --- UI Components for Different Roles ---
def admin_dashboard():
    """Dashboard for the Admin role."""
    st.title("Admin Dashboard")
    st.write("Manage users and system settings.")
    
    st.subheader("Users")
    user_data = []
    for user, data in users_db.items():
        user_data.append({"Username": user, "Role": data['role']})
    st.table(pd.DataFrame(user_data))

def teacher_dashboard():
    """Dashboard for the Teacher role."""
    st.title("Teacher Dashboard")
    st.write(f"Welcome, {st.session_state.username}!")

    menu = ["View Question Bank", "Add Question", "AI Question Generation", "Create Exam (Online)", "Create Exam Sets (Offline)"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "View Question Bank":
        st.subheader("Question Bank")
        for subject, questions in st.session_state.question_bank.items():
            st.write(f"**{subject}**")
            if questions:
                st.table(pd.DataFrame(questions))
            else:
                st.write("No questions in this bank.")

    elif choice == "Add Question":
        st.subheader("Add a New Question Manually")
        subject = st.selectbox("Select Subject", list(st.session_state.question_bank.keys()))
        question_text = st.text_area("Question Text")
        question_type = st.selectbox("Question Type", ["Short Answer", "Long Answer", "MCQ"])
        difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])
        
        if st.button("Add Question"):
            new_q = {"question": question_text, "type": question_type, "difficulty": difficulty}
            st.session_state.question_bank[subject].append(new_q)
            st.success("Question added successfully!")

    elif choice == "AI Question Generation":
        st.subheader("Generate Questions with AI")
        subject = st.text_input("Enter Topic or Subject")
        q_type = st.selectbox("Select Question Type", ["MCQ", "Short Answer", "Fill in the blank"])
        difficulty = st.select_slider("Select Difficulty", ["Easy", "Medium", "Hard"])
        
        if st.button("Generate Question"):
            if subject:
                ai_question = generate_ai_question(subject, q_type, difficulty)
                st.success("AI Generated Question:")
                st.write(ai_question)
            else:
                st.warning("Please enter a topic.")

    elif choice == "Create Exam (Online)":
        st.subheader("Create a New Digital Exam (Online)")
        exam_title = st.text_input("Exam Title (e.g., Physics Midterm)")
        subject = st.selectbox("Select Subject for Exam", list(st.session_state.question_bank.keys()))
        num_questions = st.slider("Number of Questions per Student (randomized)", 1, 10, 5)
        if subject:
            questions_df = pd.DataFrame(st.session_state.question_bank.get(subject, []))
            if not questions_df.empty:
                questions_df['Select'] = False
                edited_df = st.data_editor(questions_df, key="exam_q_selector_online")
                selected_questions = edited_df[edited_df['Select']]
                if st.button("Create Online Exam with Selected Questions"):
                    if not selected_questions.empty:
                        exam_id = f"exam_{len(st.session_state.exams) + 1}"
                        st.session_state.exams[exam_id] = {
                            "title": exam_title,
                            "subject": subject,
                            "questions": selected_questions.to_dict('records'),
                            "num_questions": num_questions
                        }
                        st.success(f"Online Exam '{exam_title}' created successfully!")
                    else:
                        st.warning("Please select at least one question.")
    elif choice == "Create Exam Sets (Offline)":
        st.subheader("Generate Multiple Unique Exam Sets for Offline Distribution")
        exam_title = st.text_input("Offline Exam Title")
        subject = st.selectbox("Select Subject for Offline Exam", list(st.session_state.question_bank.keys()), key="offline_subject")
        num_sets = st.slider("Number of Unique Sets", 2, 10, 3)
        num_questions = st.slider("Questions per Set", 1, 10, 5, key="offline_num_q")
        if st.button("Generate Offline Exam Sets"):
            all_questions = st.session_state.question_bank.get(subject, [])
            sets = []
            for i in range(num_sets):
                sets.append({
                    "set_id": f"Set-{i+1}",
                    "questions": random.sample(all_questions, min(num_questions, len(all_questions)))
                })
            st.session_state.offline_sets = sets
            st.success(f"Generated {num_sets} unique offline sets!")
            for s in sets:
                st.write(f"**{s['set_id']}**")
                for q in s['questions']:
                    st.write(q['question'])

def student_dashboard():
    """Dashboard for the Student role."""
    st.title("Student Dashboard")
    st.write(f"Welcome, {st.session_state.username}!")
    
    st.subheader("Available Exams")
    if not st.session_state.exams:
        st.info("No exams are available at the moment.")
    else:
        for exam_id, exam_details in st.session_state.exams.items():
            if st.button(f"Take Exam: {exam_details['title']}", key=exam_id):
                st.session_state.current_exam = exam_id
                # Integrate AI: Generate questions for this student
                subject = exam_details['subject']
                num_q = exam_details.get('num_questions', 5)
                difficulty = "Medium"  # You can make this dynamic
                ai_questions = generate_ai_exam_questions(subject, num_q, difficulty)
                st.session_state.student_ai_questions = ai_questions
    if 'current_exam' in st.session_state:
        exam_id = st.session_state.current_exam
        exam_details = st.session_state.exams[exam_id]
        st.subheader(f"Taking Exam: {exam_details['title']}")
        # Use AI-generated questions if available
        if 'student_ai_questions' in st.session_state:
            student_questions = st.session_state.student_ai_questions
        else:
            all_questions = exam_details['questions']
            num_q = exam_details.get('num_questions', len(all_questions))
            student_questions = random.sample(all_questions, min(num_q, len(all_questions)))
        answers = []
        with st.form(key=f"exam_form_{exam_id}"):
            for i, question in enumerate(student_questions):
                if isinstance(question, dict) and question.get('type') == 'MCQ' and 'options' in question:
                    options = question['options'][:]
                    random.shuffle(options)
                    ans = st.radio(f"Q{i+1}: {question['question']}", options, key=f"ans_{i}")
                else:
                    ans = st.text_area(f"Q{i+1}: {question if isinstance(question, str) else question['question']}", key=f"ans_{i}")
                answers.append(ans)
            submitted = st.form_submit_button("Submit Exam")
        if submitted:
            # Store submission
            if 'submissions' not in st.session_state:
                st.session_state.submissions = {}
            st.session_state.submissions.setdefault(exam_id, {})[st.session_state.username] = {
                'answers': answers,
                'questions': student_questions
            }
            st.success("Exam submitted!")
            # AI similarity check (basic)
            all_subs = st.session_state.submissions[exam_id]
            for other_user, sub in all_subs.items():
                if other_user != st.session_state.username:
                    overlap = sum([a == b for a, b in zip(answers, sub['answers'])])
                    if overlap > 0:
                        st.warning(f"Possible similarity detected with {other_user}: {overlap} identical answers.")

def main():
    """Main function to run the Streamlit app."""
    
    if not st.session_state.logged_in:
        login_page()
    else:
        st.sidebar.write(f"Role: {st.session_state.role}")
        st.sidebar.write(f"User: {st.session_state.username}")
        
        if st.sidebar.button("Logout"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

        # Display the appropriate dashboard based on the user's role
        if st.session_state.role == 'Admin':
            admin_dashboard()
        elif st.session_state.role == 'Teacher':
            teacher_dashboard()
        elif st.session_state.role == 'Student':
            student_dashboard()

if __name__ == "__main__":
    main()
