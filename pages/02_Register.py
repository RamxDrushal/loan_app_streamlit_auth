import streamlit as st
from lib.db import get_connection, ensure_users_table
from lib.auth import create_user

#  Page setup
st.set_page_config(page_title="Register", page_icon="📝", layout="centered")

#  Global CSS
st.markdown("""
<style>
/* Hide default menu/footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* App background — gradient blue */
.stApp {
  background: linear-gradient(135deg, #0f1d3b 0%, #123a6a 45%, #0f69ba 100%);
  color: #e9f2ff;
}

/* Right-align the main block and keep nice spacing from right edge */
.block-container {
  padding-top: 10rem;
  padding-bottom: 3rem;
  padding-left: 3rem;
  max-width: 720px;
  margin-left: auto;   /* push to the right */
  margin-right: 13rem; /* space from right edge */
}

/* Title */
h1, .stApp h1 {
  text-align: center;
  letter-spacing: .2px;
  color: #ffffff;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

/* --- Card (form) with glass effect --- */
[data-testid="stForm"] {
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 20px;
  padding: 32px 30px 26px 30px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
  color: #2c3e50;
}

/* Section heading inside form */
[data-testid="stForm"] h4 {
  color: #2c3e50 !important;
  font-weight: 600;
  margin-bottom: 8px;
}
[data-testid="stForm"] .stCaption, [data-testid="stForm"] p {
  color: #5a6c7d !important;
}

/* Input field labels */
.stTextInput label, .stPassword label {
  font-weight: 600 !important;
  font-size: 0.95rem !important;
  margin-bottom: 8px !important;
  color: #2c3e50 !important;
}

/* Input fields styling */
.stTextInput > div > div > input,
.stPassword > div > div > input {
  background-color: #ffffff !important;
  border: 2px solid #e1e8ed !important;
  border-radius: 10px !important;
  padding: 12px 16px !important;
  color: #2c3e50 !important;
  font-size: 0.95rem !important;
  transition: all 0.3s ease !important;
}

/* Input fields on focus */
.stTextInput > div > div > input:focus,
.stPassword > div > div > input:focus {
  border-color: #3498db !important;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1) !important;
  outline: none !important;
}

/* Placeholder */
.stTextInput > div > div > input::placeholder,
.stPassword > div > div > input::placeholder {
  color: #95a5a6 !important;
  opacity: 1 !important;
}

/* Primary button */
.stForm button[kind="primary"] {
  width: 100% !important;
  border-radius: 12px !important;
  padding: 14px 20px !important;
  font-weight: 600 !important;
  letter-spacing: 0.5px !important;
  background: linear-gradient(135deg, #3498db, #2980b9) !important;
  color: #ffffff !important;
  border: none !important;
  box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3) !important;
  transition: all 0.3s ease !important;
  font-size: 1rem !important;
  margin-top: 10px !important;
}
.stForm button[kind="primary"]:hover {
  background: linear-gradient(135deg, #2980b9, #21618c) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4) !important;
}
.stForm button[kind="primary"]:active {
  transform: translateY(0) !important;
}

/* Messages */
.stAlert[data-baseweb="notification"] {
  border-radius: 10px !important;
  margin: 10px 0 !important;
}

/* Helper note under the page */
.form-note {
  font-size: 1.2rem;
  opacity: 0.9;
  text-align: center;
  margin-top: 15px;
  color: #e9f2ff;
  text-shadow: 0 1px 2px rgba(0,0,0,0.2);
}

/* Column spacing adjustment */
[data-testid="column"] { padding: 0 8px !important; }
[data-testid="column"]:first-child { padding-left: 0 !important; }
[data-testid="column"]:last-child { padding-right: 0 !important; }

/* Left-side hero — vertically centered on the left */
.left-hero {
  position: fixed;
  left: 4rem;
  top: 50%;
  transform: translateY(-50%);   /* center vertically */
  max-width: 540px;
  color: #e9f2ff;
  z-index: 5;
}

/* Nicer headline */
.left-hero .hero-title {
  font-size: clamp(34px, 6vw, 85px);
  font-weight: 900;
  line-height: 1.05;
  letter-spacing: .3px;
  margin: 0;
  text-shadow: 0 3px 12px rgba(0,0,0,0.35);
  /* subtle gradient ink for the text */
  background: linear-gradient(180deg, #ffffff 0%, #d9ecff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

/* a tiny accent line under the title */
.left-hero .hero-title::after {
  content: "";
  display: block;
  width: 72px;
  height: 4px;
  border-radius: 999px;
  background: rgba(255,255,255,0.85);
  box-shadow: 0 2px 10px rgba(0,0,0,0.25);
  margin-top: 10px;
}

/* Keep it clean on smaller screens */
@media (max-width: 900px) {
  .left-hero {
    position: static;
    transform: none;
    margin: 1.5rem 1rem -0.5rem 1rem;
    text-align: center;
  }
  .left-hero .hero-title::after {
    margin-left: auto;
    margin-right: auto;
  }
}
}
</style>
""", unsafe_allow_html=True)

#  Left-side hero header
st.markdown("""
<div class="left-hero">
  <div class="hero-title">Welcome to<br/>Loan Eligible System</div>

</div>
""", unsafe_allow_html=True)

#  Page title above the form
st.title("Create Account")

# DB bootstrap
conn, err = get_connection()
if err:
    st.error(f"DB connection failed: {err}")
    st.stop()

tbl_err = ensure_users_table(conn)
if tbl_err:
    st.error(f"Failed to ensure users table: {tbl_err}")
    st.stop()

#  Form
with st.form("register_form", clear_on_submit=True):
    st.markdown("#### Welcome")
    st.caption("Create your account to continue.")

    name = st.text_input("Full name", placeholder="e.g., Ramosh Drushal Samarawickrama")
    email = st.text_input("Email", placeholder="you@example.com")

    col1, col2 = st.columns(2)
    with col1:
        pw1 = st.text_input("Password", type="password", placeholder="Enter password")
    with col2:
        pw2 = st.text_input("Confirm password", type="password", placeholder="Re-enter password")

    submitted = st.form_submit_button("Create Account")

#  Submission handling
if submitted:
    if not name.strip():
        st.error("Please enter your full name.")
    elif not email.strip():
        st.error("Please enter your email.")
    elif pw1 != pw2:
        st.error("Passwords do not match.")
    elif len(pw1) < 6:
        st.error("Password should be at least 6 characters.")
    else:
        ok, msg = create_user(name, email, pw1)
        if ok:
            st.success(msg + " You can now login.")
            st.balloons()
        else:
            st.error(msg)

#  Login link under the page
st.page_link("pages/01_login.py", label="Already have an account? Log in!", icon="🔑")
