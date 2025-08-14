# EduSave: AI-Powered Digital Exam System

EduSave is a Streamlit-based web application designed to minimize paper usage in academic activities by securely generating, delivering, and evaluating question papers digitally. The system ensures exam integrity, role-based access, and multi-device compatibility.

## Features
- **Role-based access:** Student, Teacher, Admin
- **AI-powered question generation:** Unique questions for each student
- **Digital exam delivery:** Online and offline exam modes
- **Anti-cheating features:** Randomized questions, answer similarity checks, multiple offline sets
- **Student portal:** View and take exams
- **Teacher portal:** Create exams, add marks, generate offline sets
- **Admin portal:** Manage users
- **User registration and login**

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd EduSave_codebase
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the Streamlit app:
```bash
streamlit run app.py
```

## Folder Structure
```
EduSave_codebase/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── users_db.json           # User database (auto-generated)
├── pages/
│   ├── student_view_questions.py  # Student question view page
│   └── teacher_add_marks.py       # Teacher marks entry page
```

## How AI is Used
- **Question Generation:** AI generates unique questions for each student based on subject and difficulty.
- **Evaluation:** AI checks for answer similarity to detect possible cheating.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
MIT
