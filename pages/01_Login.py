import time
import streamlit as st
from lib.db import get_connection, ensure_users_table
from lib.auth import authenticate

# ---------- Page setup ----------
st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")

# ---------- Global CSS (same as Register) ----------
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
  padding-top: 13rem;
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

/* Column spacing adjustment */
[data-testid="column"] { padding: 0 8px !important; }
[data-testid="column"]:first-child { padding-left: 0 !important; }
[data-testid="column"]:last-child { padding-right: 0 !important; }

/* Left-side hero — vertically centered on the left */
.left-hero {
  position: fixed;
  left: 4rem;
  top: 50%;
  transform: translateY(-50%);
  max-width: 540px;
  color: #e9f2ff;
  z-index: 5;
}

/* Hero title (same look as Register) */
.left-hero .hero-title {
  font-size: clamp(34px, 6vw, 85px);
  font-weight: 900;
  line-height: 1.05;
  letter-spacing: .3px;
  margin: 0;
  text-shadow: 0 3px 12px rgba(0,0,0,0.35);
  background: linear-gradient(180deg, #ffffff 0%, #d9ecff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

/* Tiny accent line under the title */
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

/* Responsive tweaks */
@media (max-width: 1200px) {
  .block-container { margin-right: 6rem; }
}
@media (max-width: 900px) {
  .block-container {
    margin-right: 2rem;
    padding-top: 8rem;
  }
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
@media (max-width: 640px) {
  .block-container {
    margin-right: 1rem;
    padding-left: 1rem;
    max-width: 100%;
  }
  [data-testid="column"] {
    padding-right: 4px !important;
    padding-left: 4px !important;
  }
}
</style>
""", unsafe_allow_html=True)

#  Left-side hero header
st.markdown("""
<div class="left-hero">
  <div class="hero-title">Welcome back</div>
</div>
""", unsafe_allow_html=True)

#  Page title above the form
st.title("Login")

#  DB bootstrap
conn, err = get_connection()
if err:
    st.error(f"DB connection failed: {err}")
    st.stop()

tbl_err = ensure_users_table(conn)
if tbl_err:
    st.error(f"Failed to ensure users table: {tbl_err}")
    st.stop()

#  Form
with st.form("login_form", clear_on_submit=True):
    st.markdown("#### Welcome back")
    st.caption("Sign in to continue.")
    email = st.text_input("Email", placeholder="you@example.com")
    password = st.text_input("Password", type="password", placeholder="Enter password")
    submitted = st.form_submit_button("Login")

#  Submission handling
if submitted:
    with st.spinner("Checking credentials..."):
        user, msg = authenticate(email, password)
    if user:
        st.session_state.auth = {"logged_in": True, "user": user}
        st.success("Logged in! Redirecting...")
        time.sleep(0.5)
        st.switch_page("app.py")
    else:
        st.error(msg or "Login failed.")

# Login link under the page
st.page_link("pages/02_Register.py", label="📝 Don’t have an account? Create one")




