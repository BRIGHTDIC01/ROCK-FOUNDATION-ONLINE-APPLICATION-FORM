import streamlit as st
import sqlite3
from datetime import datetime
import os
import pandas as pd
from io import BytesIO

# ---------------- DATABASE FUNCTIONS ----------------
def init_db():
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surname TEXT,
        middle_name TEXT,
        first_name TEXT,
        age INTEGER,
        class_of_entry TEXT,
        religion TEXT,
        place_of_worship TEXT,
        phone TEXT,
        state TEXT,
        local_government TEXT,
        email TEXT,
        health_issues TEXT,
        health_condition TEXT,
        sponsor_name TEXT,
        sponsor_phone TEXT,
        extracurricular TEXT,
        pledge TEXT,
        payment_proof TEXT,
        submitted_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_application(data):
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO applications (
        surname, middle_name, first_name, age, class_of_entry,
        religion, place_of_worship, phone, state, local_government,
        email, health_issues, health_condition,
        sponsor_name, sponsor_phone, extracurricular,
        pledge, payment_proof, submitted_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

init_db()

# ---------------- SIDEBAR ----------------
st.sidebar.title("MENU")
choice = st.sidebar.selectbox(
    "Choose option",
    ["Home", "Registration", "About", "Do Not Enter"],
    key="menu"
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- REGISTRATION ----------------
if choice == "Registration":

    with st.form(key="application_form"):

        st.title("STUDENT APPLICATION FORM")
        st.header("Rock Foundation Academy & College")
        st.write("Please fill in all details accurately before submission.")
        st.image("logo.jpg", width=120)

        st.subheader("Student Information")
        surname = st.text_input("Surname")
        first_name = st.text_input("First Name")
        middle_name = st.text_input("Middle Name (Optional)")
        dob = st.text_input("Month/ Day/ Year of Birth")
        age = st.slider("Age", 3, 25)
        gender = st.selectbox("Gender", ["Male", "Female"])
        nationality = st.text_input("Nationality")

        class_of_entry = st.selectbox(
            "Class of Entry",
            ["Primary 1", "Primary 2", "Primary 3", "Primary 4", "Primary 5",
             "JSS 1", "JSS 2", "JSS 3", "SSS 1", "SSS 2", "SSS 3"]
        )

        home_address = st.text_area("Home Address")

        state_of_residence = st.selectbox(
            "State of Residence",
            ["Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa",
             "Benue", "Borno", "Cross River", "Delta", "Ebonyi", "Edo",
             "Ekiti", "Enugu", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano",
             "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa",
             "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers",
             "Sokoto", "Taraba", "Yobe", "Zamfara"]
        )

        st.subheader("Parent / Guardian Information")
        guardian_name = st.text_input("Parent/Guardian Full Name")
        guardian_relationship = st.selectbox(
            "Relationship to Student",
            ["Father", "Mother", "Guardian", "Sponsor"]
        )
        guardian_phone = st.text_input("Parent/Guardian Phone Number")
        guardian_email = st.text_input("Parent/Guardian Email Address")
        guardian_occupation = st.text_input("Parent/Guardian Occupation")

        st.subheader("Previous School Information")
        previous_school = st.text_input("Name of Previous School Attended")
        school_address = st.text_area("Address of Previous School")
        last_class = st.text_input("Last Class Completed")
        reason_for_leaving = st.text_area("Reason for Leaving Previous School")

        st.subheader("Health Information")
        has_health_issues = st.selectbox(
            "Does the student have any health issues?",
            ["No", "Yes"]
        )

        if has_health_issues == "Yes":
            health_details = st.text_input("Please specify the health issue")
        else:
            health_details = "None"

        st.subheader("Academic Interests")
        vocational_skill = st.selectbox(
            "Vocational skill of interest",
            ["select option", "paint production", "Confectionary/ Baking",
             "cosmetology", "make-up", "Barbing", "Catering",
             "Hair dressing", "Arts & Craft", "Interlock production"]
        )

        career_aspiration = st.text_input(
            "Career Aspiration (What does the student want to become?)"
        )

        extracurricular = st.text_input(
            "Extra-curricular Activities (Optional)"
        )

        how_heard = st.selectbox(
            "How did you hear about our school?",
            ["Friend/Family", "Church", "Social Media", "Banner", "Other"]
        )

        additional_comments = st.text_area("Additional Comments (Optional)")

        st.subheader("Declaration")
        declaration = st.checkbox(
            "I hereby declare that the information provided is true and correct. "
            "I understand that providing false information may lead to disqualification."
        )

        st.subheader("Admission Form Fee")
        st.write("Primary= #3,000 , Secondary= #3,500")

        st.subheader(
            "Account Number 💵: 2007735304, Bank 🏦: FCMB, Account Name: ROCK-F ACADEMY LTD"
        )
        st.subheader(
            "Cross check Bank Details before initiating transactions please. NO REFUNDS"
        )
        payment_proof = st.file_uploader(
            "Attach Payment Receipt",
            type=["jpg", "png", "pdf"]
        )

        submitted = st.form_submit_button("SUBMIT APPLICATION")

    if submitted:
        if not declaration:
            st.error("You must accept the declaration.")
        elif payment_proof is None:
            st.error("Payment receipt is required.")
        else:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_path = os.path.join(
                UPLOAD_DIR, f"{surname}_{timestamp}_{payment_proof.name}"
            )

            with open(file_path, "wb") as f:
                f.write(payment_proof.getbuffer())

            insert_application((
                surname, middle_name, first_name, age, class_of_entry,
                "", "", guardian_phone, state_of_residence, "",
                guardian_email, has_health_issues, health_details,
                guardian_name, guardian_phone, extracurricular,
                "Agreed", file_path,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))

            st.success(
                "Thank you! Your application has been submitted successfully. "
                "We will contact you after review."
            )

# ---------------- HOME ----------------
elif choice == "Home":
    st.title("ROCK FOUNDATION ACADEMY STUDENT APPLICATION FORM")
    st.image("logo.jpg", width=100)
    st.header(
        "This is the official website for applicants to register for study at "
        "ROCK FOUNDATION ACADEMY AND COLLEGE"
    )
    st.subheader("To Register, Click the Menu option, Home and Registration.")
    st.image("upview.jpg", width=250)
    st.image("primary.jpg", width=250)
    st.image("secondary.jpg", width=300)
    st.image("yellow.jpg", width=350)
    st.image("blue.jpg", width=350)
# ---------------- ABOUT ----------------
elif choice == "About":
    st.header(
        "ROCK FOUNDATION ACADEMY AND COLLEGE; "
        "LAYING SOLID FOUNDATION FOR A GREAT NATION."
    )
    st.subheader("FOUNDED IN 2012.")
    st.image("logo.jpg", width=100)

    st.title("ABOUT US")
    st.header("OUR MISSION:")
    st.subheader(
        "To Provide A Conducive Learning Environment In Which Every Child "
        "Becomes Who They Ought To Be With The Help Of The Almighty God."
    )

    st.header("OUR VISION:")
    st.subheader(
        "To Produce Leaders Who Are Well Informed, Taught, And Developed "
        "Positively To Face The Future And Stand Out Amidst So Many Competitors "
        "In Their Generation."
    )

# ---------------- ADMIN PAGE ----------------
elif choice == "Do Not Enter":

    st.title("ADMIN ACCESS ONLY 🚫")

    ADMIN_PASSWORD = "Anonechonu$001."

    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    if not st.session_state.admin_authenticated:
        password = st.text_input("Enter Admin Password", type="password")

        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.success("Access granted")
            else:
                st.error("Incorrect password")
        st.stop()

    st.success("Welcome Admin")

    conn = sqlite3.connect("applications.db")
    df = pd.read_sql("SELECT * FROM applications", conn)
    conn.close()

    if df.empty:
        st.warning("No applications found.")
    else:
        st.dataframe(df)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False)

        output.seek(0)

        st.download_button(
            "Download as Excel",
            data=output,
            file_name="applications.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
