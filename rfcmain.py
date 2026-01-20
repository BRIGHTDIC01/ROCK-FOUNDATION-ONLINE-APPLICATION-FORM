import os

import streamlit as st
import sqlite3
from datetime import datetime
import os
import pandas as pd
from io import BytesIO

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Rock Foundation Academy", layout="centered")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ADMIN_PASSWORD = "Anonechonu$001."


# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("applications.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surname TEXT,
        first_name TEXT,
        middle_name TEXT,
        dob TEXT,
        age INTEGER,
        gender TEXT,
        nationality TEXT,
        class_of_entry TEXT,
        home_address TEXT,
        state_of_residence TEXT,
        guardian_name TEXT,
        guardian_relationship TEXT,
        guardian_phone TEXT,
        guardian_email TEXT,
        guardian_occupation TEXT,
        previous_school TEXT,
        school_address TEXT,
        last_class TEXT,
        reason_for_leaving TEXT,
        health_issues TEXT,
        health_details TEXT,
        vocational_skill TEXT,
        career_aspiration TEXT,
        extracurricular TEXT,
        how_heard TEXT,
        additional_comments TEXT,
        declaration TEXT,
        payment_proof TEXT,
        submitted_at TEXT
    )
    """)
    conn.commit()
    conn.close()


def insert_application(data):
    conn = sqlite3.connect("applications.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO applications (
            surname, first_name, middle_name, dob, age, gender, nationality,
            class_of_entry, home_address, state_of_residence,
            guardian_name, guardian_relationship, guardian_phone,
            guardian_email, guardian_occupation,
            previous_school, school_address, last_class, reason_for_leaving,
            health_issues, health_details, vocational_skill,
            career_aspiration, extracurricular, how_heard,
            additional_comments, declaration, payment_proof, submitted_at
        ) VALUES (
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?
        )
    """, data)

    conn.commit()
    conn.close()


init_db()

# ---------------- QUERY PARAMS ----------------
params = st.experimental_get_query_params()
is_admin = params.get("admin", ["false"])[0].lower() == "true"


# ---------------- SIDEBAR ----------------
menu_options = ["Home", "Registration", "About"]
if is_admin:
    menu_options.append("Do Not Enter")

choice = st.sidebar.selectbox("Choose option", menu_options)


# ---------------- HOME ----------------
if choice == "Home":
    st.title("ROCK FOUNDATION ACADEMY & COLLEGE")
    st.image("logo.jpg", width=120)
    st.header("Official Online Admission Portal")
    st.write("To Apply For Admission, Use The Menu Button And Select Register.")
    st.image("upview.jpg", width=300)
    st.image("secondary.jpg", width=350)
    st.image("primary.jpg", width=350)
    st.image("blue.jpg", width=400)
    st.image("yellow.jpg", width=400)


# ---------------- ABOUT ----------------
elif choice == "About":
    st.image("logo.jpg", width=120)
    st.header("ABOUT US")
    st.header("ROCK FOUNDATION ACADEMY AND COLLEGE was founded in 2012.")
    st.header("MISSION")
    st.subheader(
        "To Provide A Conducive Learning Environment In Which Every Child Becomes Who They Ought To Be With The Help Of The Almighty God"
    )
    st.header("VISION")
    st.subheader(
        "To Produce Leaders Who Are Well Informed,Taught, And Developed Positively To Face The Future And Stand Out Admist So Many Competitors In Their Generations."
    )

# ---------------- REGISTRATION ----------------
elif choice == "Registration":
    st.title("ONLINE APPLICATION FORM")

    with st.form("application_form"):
        st.title("STUDENT'S INFORMATION")

        surname = st.text_input("Surname")
        first_name = st.text_input("First Name")
        middle_name = st.text_input("Middle Name (Optional)")
        dob = st.text_input("Month/ Day/ Year of Birth")
        age = st.slider("Age", 3, 25)
        gender = st.selectbox("Gender", ["Male", "Female"])
        nationality = st.text_input("Nationality")

        class_of_entry = st.selectbox(
            "Class of Entry",
            ["Primary 1","Primary 2","Primary 3","Primary 4","Primary 5",
             "JSS 1","JSS 2","JSS 3","SSS 1","SSS 2","SSS 3"]
        )

        home_address = st.text_area("Home Address")
        state_of_residence = st.text_input("State of Residence")

        st.title("PARENT'S/ GUARDIAN'S INFORMATION")

        guardian_name = st.text_input("Parent/Guardian Full Name")
        guardian_relationship = st.selectbox(
            "Relationship to Student",
            ["Father", "Mother", "Guardian", "Sponsor"]
        )
        guardian_phone = st.text_input("Parent/Guardian Phone Number")
        guardian_email = st.text_input("Parent/Guardian Email Address")
        guardian_occupation = st.text_input("Parent/Guardian Occupation")

        st.title("PREVIOUS SCHOOL INFORMATION")

        previous_school = st.text_input("Name of Previous School Attended")
        school_address = st.text_area("Address of Previous School")
        last_class = st.text_input("Last Class Completed")
        reason_for_leaving = st.text_area("Reason for Leaving Previous School")

        has_health_issues = st.selectbox(
            "Does the student have any health issues?",
            ["No", "Yes"]
        )

        if has_health_issues == "Yes":
            health_details = st.text_input("Please specify the health issue")
        else:
            health_details = "None"

        st.title("STUDENT'S INTEREST")

        vocational_skill = st.text_input("Vocational skill of interest")
        career_aspiration = st.text_input("Career Aspiration")
        extracurricular = st.text_input("Extra-curricular Activities")
        how_heard = st.text_input("How did you hear about our school?")
        additional_comments = st.text_area("Additional Comments")

        declaration = st.checkbox(
            "I hereby declare that the information provided is correct"
        )

        st.subheader("Admission Form Fee")
        st.write("Primary= #3,000 , Secondary= #3,500")

        st.subheader(
            "Account Number 🏦: 2007735304, Bank 🏦: FCMB, Account Name: ROCK-F ACADEMY LTD"
        )
        st.subheader("Cross check Bank Details before initiating transactions please. NO REFUNDS")
        payment_proof = st.file_uploader(
            "Attach Payment Receipt", type=["jpg","png","pdf"]
        )

        submitted = st.form_submit_button("SUBMIT APPLICATION")

    if submitted:
        if not declaration or not payment_proof:
            st.error("Declaration and payment receipt are required.")
        else:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_path = os.path.join(
                UPLOAD_DIR, f"{surname}_{timestamp}_{payment_proof.name}"
            )

            with open(file_path, "wb") as f:
                f.write(payment_proof.getbuffer())

            insert_application((
                surname, first_name, middle_name, dob, age, gender, nationality,
                class_of_entry, home_address, state_of_residence,
                guardian_name, guardian_relationship, guardian_phone,
                guardian_email, guardian_occupation,
                previous_school, school_address, last_class, reason_for_leaving,
                has_health_issues, health_details, vocational_skill,
                career_aspiration, extracurricular, how_heard,
                additional_comments, "Agreed", file_path,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))

            st.success("Application submitted successfully!")


# ---------------- ADMIN ----------------
elif choice == "Do Not Enter":

    password = st.text_input("Admin Password", type="password")
    if password != ADMIN_PASSWORD:
        st.stop()

    st.title("ADMIN DASHBOARD")

    conn = sqlite3.connect("applications.db")
    df = pd.read_sql("SELECT * FROM applications", conn)
    conn.close()

    st.dataframe(df)

    # ---------- VIEW PAYMENT PROOF ----------
    st.subheader("View Payment Proof")

    if df.empty:
        st.info("No applications submitted yet.")
        st.stop()

    app_id = st.selectbox("Select Application ID", df["id"])

    proof_path = df[df["id"] == app_id]["payment_proof"].values[0]

    if proof_path and os.path.exists(proof_path):
        if proof_path.lower().endswith((".jpg", ".jpeg", ".png")):
            st.image(proof_path, caption="Payment Receipt", width=400)

        elif proof_path.lower().endswith(".pdf"):
            with open(proof_path, "rb") as f:
                st.download_button(
                    "Download Payment Receipt (PDF)",
                    data=f,
                    file_name=os.path.basename(proof_path),
                    mime="application/pdf"
                )
    else:
        st.warning("Payment proof file not found.")
