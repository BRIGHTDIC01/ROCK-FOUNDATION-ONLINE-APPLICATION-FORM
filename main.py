import streamlit as st

st.sidebar.title("MENU")
choice = st.sidebar.selectbox("choose option", ["Home", "Registration"])
if choice == "Registration":
    st.title("APPLICATION FORM")
    st.header("Fill in all details Accurately before submission")
    st.image("logo.jpg", width=100)
    sname = st.text_input("Enter your surname")
    fname = st.text_input("Enter your first name")
    mname = st.text_input("Enter your middle name")
    st.write("Hello,", sname, mname, fname)
    age = st.slider("Select Your Age",0, 30, 8)
    st.write("Your age is:", age)
    religion = st.selectbox("Religion", ["christian", "muslim"])
    if religion == "christian":
        st.text_input("place of worship")
    phone = st.text_input("Enter your phone number")
    state = st.text_input("Enter your state of origin")
    local = st.text_input("Enter your local government of origin")
    email = st.text_input("Enter email adress")
    doc = st.file_uploader("upload a document of your last result (IF ANY)")
    doc2 = st.file_uploader("upload a passport photograph of yourself")
    health = st.selectbox("Do you have health issues?", ["yes", "No"])
    if health == "yes":
        st.text_input("please specify area")
        name2 = st.text_input("Enter sponsor's full name")
        num = st.text_input("Enter sponsor's phone number")
        st.text_input("Extra-curricular activity (IF ANY, can be more than 1)")
        st.write("If given admission into Rock Foundation Academy and College, Do you promise to Abide by every rule and regulation set by the school?")
        st.checkbox("Yes"), st.checkbox("No")
        st.write("For more Enquiry call; 08065472739, 08036344669.")
if choice == "Home":
    st.title("ROCK FOUNDATION ACADEMY STUDENT APPLICATION FORM")
    st.image("logo.jpg", width=100)
    st.header("This is the official website for applicants to register for study at ROCK FOUNDATION ACADEMY AND COLLEGE")
    st.subheader("To Register, Click the Menu option, Home and Registration.")
    st.image("upview.jpg", width=300)
    st.image("primary.jpg", width=350)
    st.image("secondary.jpg", width=350)
    st.image("yellow.jpg", width=400)
    st.image("blue.jpg", width=400)










