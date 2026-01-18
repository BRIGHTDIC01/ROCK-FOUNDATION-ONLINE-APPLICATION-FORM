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
        ?,?,?,?,?,?,?,?,?,?
    )
    """, data)
    conn.commit()
    conn.close()


init_db()

# ---------------- QUERY PARAMS ----------------
params = st.experimental_get_query_params()
is_admin = params.get("admin", ["false"])[0].lower() == "true"


# ---------------- SIDEBAR ----------------
if is_admin:
    menu_options = ["Home", "Registration", "About", "Do Not Enter"]
else:
    menu_options = ["Home", "Registration", "About"]

choice = st.sidebar.selectbox("Choose option", menu_options, key="menu")


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
        st.file_uploader("Upload Applicant's passport photograph")

        class_of_entry = st.selectbox(
            "Class of Entry",
            ["Primary 1","Primary 2","Primary 3","Primary 4","Primary 5",
             "JSS 1","JSS 2","JSS 3","SSS 1","SSS 2","SSS 3"]
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
        st.file_uploader("Upload an image of Applicant's Last Result sheet")
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
        health_issues = has_health_issues

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

        extracurricular = st.text_input("Extra-curricular Activities (Optional)")
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
            "Account Number 🏦: 2007735304, Bank 🏦: FCMB, Account Name: ROCK-F ACADEMY LTD"
        )
        st.subheader("Cross check Bank Details before initiating transactions please. NO REFUNDS")

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
                surname, first_name, middle_name, dob, age, gender,
                nationality, class_of_entry, home_address, state_of_residence,
                guardian_name, guardian_relationship, guardian_phone,
                guardian_email, guardian_occupation,
                previous_school, school_address, last_class, reason_for_leaving,
                health_issues, health_details, vocational_skill,
                career_aspiration, extracurricular, how_heard,
                additional_comments, "Agreed", file_path,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))

            st.success(
                "Thank you! Your application has been submitted successfully. "
                "We will contact you after review."
            )


# ---------------- ADMIN ----------------
elif choice == "Do Not Enter":

    if "admin" not in st.session_state:
        st.session_state.admin = False

    if not st.session_state.admin:
        password = st.text_input("Admin Password", type="password")
        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.admin = True
                st.success("Access granted")
            else:
                st.error("Incorrect password")
        st.stop()

    st.title("ADMIN DASHBOARD")

    conn = sqlite3.connect("applications.db")
    df = pd.read_sql("SELECT * FROM applications", conn)
    conn.close()

    st.dataframe(df)

    st.subheader("View Payment Proof")
    app_id = st.selectbox("Select Application ID", df["id"])

    proof = df[df["id"] == app_id]["payment_proof"].values[0]
    if os.path.exists(proof):
        if proof.endswith((".jpg",".png")):
            st.image(proof, width=400)
        else:
            with open(proof,"rb") as f:
                st.download_button(
                    "Download Receipt",
                    f,
                    file_name=os.path.basename(proof)
                )

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    st.download_button(
        "Download All Applications (Excel)",
        data=output,
        file_name="applications.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
