import streamlit as st
import pandas as pd
import numpy as np
import joblib
import mysql.connector
from datetime import datetime

# Page configuration

st.set_page_config(
    page_title="Loan Department",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

AMOUNT_TOLERANCE = 50_000
REQUIRED_CREDIT_SCORE = 700
CREDIT_SCORE_TOLERANCE = 20

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'RootPassword1',
    'database': 'loan_app'
}

CLASSIFIER_PKL = r"E:\Loan Model\best_loan_model.pkl"
SCALER_PKL     = r"E:\Loan Model\scaler.pkl"
HYBRID_PKL     = r"E:\Loan Model\hybrid_pipeline.pkl"


CAT_COLS = [
    'Gender', 'Marital_Status', 'Education', 'Employment_Status',
    'Residential_Status', 'Loan_Purpose'
]
NUMERICAL_COLS = [
    'Age', 'Dependents', 'Annual_Income', 'Monthly_Income',
    'Credit_Score', 'Existing_Loans', 'Total_Existing_Loan_Amount',
    'Loan_Amount_Requested', 'Loan_Term', 'Bank_Account_History'
]

ENCODERS = {
    'Gender': {'Male': 1, 'Female': 0},
    'Marital_Status': {'Married': 1, 'Single': 0, 'Divorced': 2},
    'Education': {'Graduate': 1, 'Undergraduate': 0, 'High School': 2},
    'Employment_Status': {'Employed': 1, 'Self-Employed': 0, 'Unemployed': 2},
    'Residential_Status': {'Own': 1, 'Rent': 0, 'Family': 2},
    'Loan_Purpose': {
        'Small Business Start-up': 0,
        'Equipment Purchase': 1,
        'Working Capital': 2,
        'Expansion': 3,
        'Other': 4
    }
}


# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');

    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; scroll-behavior: smooth; }

    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #6B73FF, #9A9CE3);
        background-size: 200% 200%;
        min-height: 100vh; position: relative;
    }
    .stApp::before { content: ''; position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.1); pointer-events:none; z-index:1; }

    .main { position:relative; z-index:2; padding: 2rem 1rem !important; }
    .block-container { padding-top:1rem !important; padding-bottom:11rem !important; max-width:1600px !important; position:relative; z-index:2; }

    .header-container {
        background: rgba(255,255,255,0.15); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2); border-radius: 24px; padding: 2rem 2.5rem; margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15), inset 0 1px 0 rgba(255,255,255,0.3);
        transition: all .3s cubic-bezier(0.4,0,0.2,1); position: relative; overflow:hidden;
    }
    .header-container::before {
        content: ''; position: absolute; top:0; left:0; right:0; height:3px;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4, #FFEAA7); background-size: 300% 100%;
    }
    .header-title {
        color: #fff !important; font-family: 'Poppins', sans-serif !important; font-size: 2.5rem !important; font-weight: 700 !important;
        margin: 0 !important; text-shadow: 0 4px 20px rgba(0,0,0,0.3); display:flex !important; align-items:center !important; gap: 1rem !important; letter-spacing: -0.5px !important;
    }

    .form-section {
        background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.3); border-radius: 20px; padding: 2rem 2.5rem; margin-bottom: 1.5rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1), inset 0 1px 0 rgba(255,255,255,0.6);
        transition: all .4s cubic-bezier(0.4,0,0.2,1); position: relative; overflow: hidden;
    }
    .form-section::before {
        content: ''; position: absolute; top:0; left:0; right:0; height:4px;
        background: linear-gradient(90deg, #FF9A9E, #FECFEF, #FECFEF, #FF9A9E); border-radius: 20px 20px 0 0; opacity:.8;
    }
    .section-title {
        color:#2D3748 !important; font-family:'Poppins', sans-serif !important; font-size:1.4rem !important; font-weight:600 !important;
        margin-bottom:1.5rem !important; padding-bottom:.8rem !important; border-bottom:3px solid transparent !important;
        background: linear-gradient(90deg, #667eea, #764ba2) !important; background-clip:text !important; -webkit-background-clip:text !important; -webkit-text-fill-color:transparent !important; position:relative;
    }
    .section-title::after { content:''; position:absolute; bottom:-3px; left:0; width:60px; height:3px; background: linear-gradient(90deg, #667eea, #764ba2); border-radius:2px; transition: width .3s ease; }
    .form-section:hover .section-title::after { width:120px; }

    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.9) !important; color:#2D3748 !important; border:2px solid rgba(102,126,234,0.2) !important;
        border-radius: 12px !important; padding:1rem 1.2rem !important; font-size:1rem !important; font-weight:500 !important;
        transition: all .3s cubic-bezier(0.4,0,0.2,1) !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05), inset 0 1px 0 rgba(255,255,255,0.8) !important;
        height:auto !important; min-height:3rem !important; backdrop-filter: blur(10px) !important;
    }

    .stSelectbox > div > div > div {
        background: rgba(255,255,255,0.9) !important; color:#2D3748 !important; border:2px solid rgba(102,126,234,0.2) !important;
        border-radius: 12px !important; font-weight:500 !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05), inset 0 1px 0 rgba(255,255,255,0.8) !important;
        transition: all .3s cubic-bezier(0.4,0,0.2,1) !important; font-size:1rem !important; min-height:3rem !important; backdrop-filter: blur(10px) !important;
    }

    .stRadio > div { background: transparent !important; padding:.5rem 0 !important; }
    .stRadio > div > label { color:#2D3748 !important; font-weight:600 !important; font-size:1rem !important; margin-bottom:1rem !important; }
    .stRadio > div > div { flex-direction: row !important; gap:1rem !important; margin-top:.5rem !important; }
    .stRadio > div > div > label {
        background: rgba(255,255,255,0.9) !important; padding:.8rem 1.5rem !important; border:2px solid rgba(102,126,234,0.2) !important; border-radius:12px !important; cursor:pointer !important;
        transition: all .3s cubic-bezier(0.4,0,0.2,1) !important; font-weight:500 !important; color:#4A5568 !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05), inset 0 1px 0 rgba(255,255,255,0.8) !important;
        font-size:.9rem !important; backdrop-filter: blur(10px) !important; min-width: fit-content !important;
    }
    .stRadio > div > div > label:hover { border-color:#667eea !important; background: rgba(102,126,234,0.05) !important; transform: translateY(-3px) scale(1.05) !important; box-shadow: 0 10px 30px rgba(102,126,234,0.2) !important; }

    .stTextInput > label, .stNumberInput > label, .stRadio > label, .stSelectbox > label {
        color:#2D3748 !important; font-weight:600 !important; letter-spacing:.3px !important; text-transform: uppercase !important; font-size:.85rem !important; margin-bottom:.8rem !important;
    }

    .stButton > button {
        border-radius: 16px !important; font-weight:600 !important; font-size:1.1rem !important; height:3.5rem !important;
        transition: all .4s cubic-bezier(0.4,0,0.2,1) !important; border:none !important; letter-spacing:.5px !important; text-transform: uppercase !important; position:relative !important; overflow:hidden !important; backdrop-filter: blur(10px) !important;
    }
    .stButton > button::before {
        content:''; position:absolute; top:0; left:-100%; width:100%; height:100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent); transition: left .6s ease;
    }
    .stButton > button:hover::before { left: 100%; }
    .stButton > button[kind="primary"] { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; color:#fff !important; box-shadow: 0 8px 30px rgba(102,126,234,0.4), inset 0 1px 0 rgba(255,255,255,0.2) !important; }
    .stButton > button[kind="secondary"] { background: linear-gradient(135deg, #718096 0%, #4A5568 100%) !important; color:#fff !important; box-shadow: 0 8px 30px rgba(113,128,150,0.4), inset 0 1px 0 rgba(255,255,255,0.2) !important; }

    .result-success, .result-error, .result-info {
        border-radius: 20px; padding: 2.5rem 3rem; margin: 2rem 0; position: relative; overflow: hidden; animation: slideInUp .6s ease;
        backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    }
    .result-success { background: linear-gradient(135deg, rgba(72,187,120,.15) 0%, rgba(56,178,172,.15) 100%); border: 2px solid rgba(72,187,120,.3); color:#22543D; }
    .result-error   { background: linear-gradient(135deg, rgba(245,101,101,.15) 0%, rgba(229,62,62,.15) 100%); border: 2px solid rgba(245,101,101,.3); color:#742A2A; }
    .result-info {
        background: transparent !important;
        border: none !important;
        border-top: 4px solid #0f1d3b !important;
        padding: 1rem 0 0 0 !important;
        margin-top: 1.5rem !important;
        color: #0f1d3b !important;
        text-align: center;
    }

    /* New combined error-suggestion box */
    .result-combined {
        background: linear-gradient(135deg, rgba(245,101,101,.15) 0%, rgba(229,62,62,.15) 100%);
        border: 2px solid rgba(245,101,101,.3);
        border-radius: 20px;
        padding: 2.5rem 3rem;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
        animation: slideInUp .6s ease;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        color: #742A2A;
    }

    .combined-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 2rem;
    }

    .combined-left h3 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
    }

    .combined-right {
        text-align: center;
    }

    .combined-right h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
        font-weight: 600;
    }

    .combined-right .amount {
        font-size: 2rem;
        font-weight: bold;
        color: #742A2A;
        margin: 0;
    }

    @keyframes slideInUp { from { transform: translateY(30px); opacity:0; } to { transform: translateY(0); opacity:1; } }
    [data-testid="column"] { padding: .5rem !important; }

    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} .stDeployButton {visibility: hidden;}

    @media (max-width: 1200px) {
        .header-title { font-size: 2rem !important; }
        .form-section { padding: 1.5rem 2rem !important; }
        .section-title { font-size: 1rem !important; }
        .combined-content { flex-direction: column; text-align: center; gap: 1rem; }
        .combined-right .amount { font-size: 1.5rem; }
    }
    @media (max-width: 768px)  {
        .header-title { font-size: 1.5rem !important; }
        .form-section { padding: 1.2rem 1.5rem !important; }
        .result-success, .result-error, .result-info, .result-combined { padding: 1rem 1rem !important; }
        .combined-content { gap: 0.5rem; }
        .combined-right .amount { font-size: 1.3rem; }
    }
</style>
""", unsafe_allow_html=True)

# Logout
def _logout_and_go_to_login():
    """Clear session state and navigate to the Login page."""
    # Clear session state
    for k in list(st.session_state.keys()):
        try:
            del st.session_state[k]
        except Exception:
            pass

    # Ensure flags reset
    st.session_state["eligibility_checked"] = False

    # Try to switch page to Login
    try:
        # Works in modern Streamlit multipage apps
        st.switch_page("pages/01_Login.py")
    except Exception:
        # Fallback: show a safe link
        st.session_state["_show_login_link"] = True
        st.rerun()

# Model loader
@st.cache_resource
def load_models():
    """Load all models with caching to improve performance."""
    try:
        clf_model = joblib.load(CLASSIFIER_PKL)
        clf_scaler = joblib.load(SCALER_PKL)
        hybrid_model = joblib.load(HYBRID_PKL)
        return clf_model, clf_scaler, hybrid_model, None
    except FileNotFoundError as e:
        return None, None, None, str(e)

# DB utilities

def save_to_database(user_input, result):
    """Save user input and assessment results to MySQL database."""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        sql = """
            INSERT INTO data (
                id, name, gender, age, marital_status, dependents, education, employment_status,
                residential_status, annual_income, monthly_income, credit_score, existing_loans,
                total_existing_loan_amount, loan_amount_requested, loan_term, loan_purpose,
                bank_account_history, eligibility, confidence, suggested_amount, final_eligibility,
                final_confidence, approved_amount, created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            None,  # id (auto-increment)
            user_input['name'],
            user_input['Gender'],
            user_input['Age'],
            user_input['Marital_Status'],
            user_input['Dependents'],
            user_input['Education'],
            user_input['Employment_Status'],
            user_input['Residential_Status'],
            user_input['Annual_Income'],
            user_input['Monthly_Income'],
            user_input['Credit_Score'],
            user_input['Existing_Loans'],
            user_input['Total_Existing_Loan_Amount'],
            user_input['Loan_Amount_Requested'],
            user_input['Loan_Term'],
            user_input['Loan_Purpose'],
            user_input['Bank_Account_History'],
            result['eligibility'],
            result['confidence'] if result['confidence'] is not None else None,
            result['suggested_amount'] if result['suggested_amount'] is not None else None,
            result['final_eligibility'],
            result['final_confidence'] if result['final_confidence'] is not None else None,
            result['approved_amount'] if result['approved_amount'] is not None else None,
            datetime.now()
        )
        cursor.execute(sql, values)
        conn.commit()
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
    finally:
        try:
            if cursor: cursor.close()
            if conn: conn.close()
        except Exception:
            pass


def get_previous_suggestion(applicant_name):
    """Fetch the most recent suggested amount for this applicant (if any)."""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT suggested_amount
            FROM data
            WHERE name = %s
              AND suggested_amount IS NOT NULL
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (applicant_name,)
        )
        row = cursor.fetchone()
        return float(row[0]) if row and row[0] is not None else None
    except mysql.connector.Error as err:
        st.error(f"Database error (fetch suggestion): {err}")
        return None
    finally:
        try:
            if cursor: cursor.close()
            if conn: conn.close()
        except Exception:
            pass

# Core assessment logic

def assess_and_suggest(
    user_input,
    clf_model,
    clf_scaler,
    hybrid_model,
    cap_at_requested=True,
    round_to=1000,
    prev_suggested_amount=None,
):
    """Assessment + hybrid suggestion + rule-based overrides."""

    clf_feature_order = [
        'Gender', 'Age', 'Marital_Status', 'Dependents', 'Education', 'Employment_Status',
        'Residential_Status', 'Annual_Income', 'Monthly_Income', 'Credit_Score',
        'Existing_Loans', 'Total_Existing_Loan_Amount', 'Loan_Amount_Requested',
        'Loan_Term', 'Loan_Purpose', 'Bank_Account_History'
    ]

    Xclf_raw = pd.DataFrame([user_input], columns=clf_feature_order)

    # Encode categoricals
    Xclf = Xclf_raw.copy()
    for col in CAT_COLS:
        if col in Xclf.columns:
            Xclf[col] = Xclf[col].map(ENCODERS[col])

    # Scale numerics
    available_num_cols = [col for col in NUMERICAL_COLS if col in Xclf.columns]
    Xclf[available_num_cols] = clf_scaler.transform(Xclf[available_num_cols])

    # Predict eligibility at requested amount
    y_pred = clf_model.predict(Xclf)[0]
    proba = clf_model.predict_proba(Xclf)[0, 1] if hasattr(clf_model, 'predict_proba') else None
    eligibility = 'Eligible' if y_pred == 1 else 'Not Eligible'

    result = {
        "eligibility": eligibility,
        "confidence": float(proba) if proba is not None else None,
        "suggested_amount": None,
        "cluster": None,
        "regression_model": None,
        "final_eligibility": eligibility,
        "final_confidence": float(proba) if proba is not None else None,
        "approved_amount": user_input['Loan_Amount_Requested'] if y_pred == 1 else None
    }

    # Hybrid suggestion if not eligible
    if y_pred == 0 and hybrid_model:
        try:
            reg_cols = hybrid_model["reg_num_cols"] + hybrid_model["cat_cols"]
            Xreg_raw = pd.DataFrame([{col: user_input.get(col) for col in reg_cols}])

            for col in hybrid_model["cat_cols"]:
                if col in hybrid_model["enc_maps"]:
                    Xreg_raw[col] = Xreg_raw[col].map(hybrid_model["enc_maps"][col])

            # Stage-1: Cluster
            Xn = hybrid_model["scaler"].transform(Xreg_raw[hybrid_model["reg_num_cols"]])
            Xc = Xreg_raw[hybrid_model["cat_cols"]].values
            X_for_cluster = np.hstack([Xn, Xc])
            cluster_id = int(hybrid_model["kmeans"].predict(X_for_cluster)[0])

            # Stage-2: Regression
            onehot = np.zeros((1, hybrid_model["n_clusters"]), dtype=float)
            onehot[0, cluster_id] = 1.0
            X_reg_in = np.hstack([Xn, Xc, onehot])
            pred_amount = float(hybrid_model["reg_model"].predict(X_reg_in)[0])

            # Cap and round
            requested = float(user_input.get('Loan_Amount_Requested', pred_amount))
            if cap_at_requested:
                pred_amount = min(pred_amount, requested)
            if round_to and round_to > 0:
                pred_amount = round(pred_amount / round_to) * round_to

            result["suggested_amount"] = pred_amount
            result["cluster"] = cluster_id
            result["regression_model"] = type(hybrid_model["reg_model"]).__name__

            # Re-check eligibility at suggested amount
            updated_input = user_input.copy()
            updated_input['Loan_Amount_Requested'] = pred_amount
            Xclf_raw_updated = pd.DataFrame([updated_input], columns=clf_feature_order)

            Xclf_updated = Xclf_raw_updated.copy()
            for col in CAT_COLS:
                if col in Xclf_updated.columns:
                    Xclf_updated[col] = Xclf_updated[col].map(ENCODERS[col])
            Xclf_updated[available_num_cols] = clf_scaler.transform(Xclf_updated[available_num_cols])

            y_pred_updated = clf_model.predict(Xclf_updated)[0]
            proba_updated = clf_model.predict_proba(Xclf_updated)[0, 1] if hasattr(clf_model, 'predict_proba') else None
            final_eligibility = 'Eligible' if y_pred_updated == 1 else 'Not Eligible'

            result["final_eligibility"] = final_eligibility
            result["final_confidence"] = float(proba_updated) if proba_updated is not None else None
            result["approved_amount"] = pred_amount if y_pred_updated == 1 else None

        except Exception as e:
            st.error(f"Error in hybrid model processing: {e}")

    # ---- RULE-BASED OVERRIDES ----
    requested_amt = float(user_input.get('Loan_Amount_Requested', 0.0))
    credit_score = float(user_input.get('Credit_Score', 0.0))

    def within_amount_tolerance(base, candidate, tol=AMOUNT_TOLERANCE):
        if base is None or candidate is None:
            return False
        return abs(float(candidate) - float(base)) <= float(tol)

    def within_credit_tolerance(score, required=REQUIRED_CREDIT_SCORE, tol=CREDIT_SCORE_TOLERANCE):
        if score is None:
            return False
        return abs(float(score) - float(required)) <= float(tol)

    amount_ok_current = within_amount_tolerance(result["suggested_amount"], requested_amt)
    amount_ok_previous = within_amount_tolerance(prev_suggested_amount, requested_amt)
    credit_ok = within_credit_tolerance(credit_score)

    if amount_ok_current or amount_ok_previous or credit_ok:
        result["eligibility"] = "Eligible"
        result["final_eligibility"] = "Eligible"
        if result.get("final_confidence") is None and result.get("confidence") is not None:
            result["final_confidence"] = result["confidence"]
        result["approved_amount"] = requested_amt

    return result

# Home page
def main():
    # Init state
    if 'eligibility_checked' not in st.session_state:
        st.session_state.eligibility_checked = False

    # Load models
    clf_model, clf_scaler, hybrid_model, error = load_models()
    if error:
        st.markdown(f"""
        <div class="result-error">
            <h3>Model Loading Error</h3>
            <p>{error}</p>
            <p>Please ensure all pickle files are in the correct directory</p>
        </div>
        """, unsafe_allow_html=True)
        # Even if models failed, still show logout link if needed
        if st.session_state.get("_show_login_link"):
            st.page_link("pages/01_Login.py", label="Go to Login", icon="🔑")
        return

    # Header row with right-aligned Logout
    left_col, right_col = st.columns([6, 1], gap="small")
    with left_col:
        st.markdown("""
        <div class="header-container">
            <h1 class="header-title">🏦 Loan Department - Application Form</h1>
        </div>
        """, unsafe_allow_html=True)
    with right_col:
        st.markdown("<div style='height: 22px'></div>", unsafe_allow_html=True)  # vertical align
        if st.button("🚪 Logout", type="secondary", use_container_width=True, key="logout_btn"):
            _logout_and_go_to_login()

    # Fallback login link if switch_page not available
    if st.session_state.get("_show_login_link"):
        st.page_link("pages/01_Login.py", label="Go to Login", icon="🔑")

    # ---- Form Columns ----
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1], gap="medium")

    with col1:
        st.markdown('<div class="form-section"><div class="section-title">Applicant Details</div>', unsafe_allow_html=True)
        name = st.text_input("Name", placeholder="Enter your full name", key="name_input")
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True, key="gender_input")
        age = st.number_input("Age", min_value=20, max_value=60, step=1, key="age_input")
        marital_status = st.radio("Marital Status", ["Single", "Married"], horizontal=True, key="marital_input")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="form-section"><div class="section-title">Background Information</div>', unsafe_allow_html=True)
        dependents = st.number_input("Dependents", min_value=0, max_value=3, step=1, key="dependents_input")
        education = st.text_input("Education", placeholder="e.g., Graduate, Undergraduate", key="education_input")
        employee_status = st.text_input("Employee Status", placeholder="e.g., Employed, Self-Employed", key="employee_input")
        resident_status = st.radio("Resident Status", ["Own", "Rent", "Family"], horizontal=True, key="resident_input")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="form-section"><div class="section-title">Loan Details</div>', unsafe_allow_html=True)
        loan_purpose = st.selectbox(
            "Loan Purpose",
            ['Small Business Start-up', 'Equipment Purchase', 'Working Capital', 'Expansion', 'Other'],
            key="loan_purpose_input"
        )
        requested_amount = st.number_input("Requested Amount", min_value=100000, max_value=1000000, step=10000, format="%d", key="requested_amount_input")
        loan_terms = st.number_input("Loan Terms (months)", min_value=12, max_value=96, step=1, key="loan_terms_input")
        bank_account_history = st.number_input("Bank Account History (years)", min_value=0, max_value=10, step=1, key="bank_account_history_input")
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="form-section"><div class="section-title">Financial Details</div>', unsafe_allow_html=True)
        annual_income = st.number_input("Annual Income", min_value=100000, max_value=800000, step=10000, format="%d", key="annual_income_input")
        monthly_income = st.number_input("Monthly Income", min_value=10000, max_value=300000, step=1000, format="%d", key="monthly_income_input")
        credit_score = st.number_input("Credit Score", min_value=300, max_value=830, step=1, key="credit_score_input")
        existing_loans = st.number_input("Existing Loans", min_value=0, max_value=10, step=1, key="existing_loans_input")
        existing_loan_amount = st.number_input("Existing Loan Amount", min_value=0, step=1000, format="%d", key="existing_amount_input")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---- Buttons ----
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        check_eligibility = st.button("🔍 Check Eligibility", type="primary", use_container_width=True, key="check_button")
    with c3:
        reset_form = st.button("🔄 Reset Form", use_container_width=True, key="reset_button")
    st.markdown("</div>", unsafe_allow_html=True)

    # ---- Handlers ----
    if check_eligibility and not st.session_state.eligibility_checked:
        # Basic validations
        if not name.strip():
            st.markdown("""
            <div class="result-error">
                <h4>Validation Error</h4>
                <p>Please enter your name</p>
            </div>
            """, unsafe_allow_html=True)
            return

        if not education.strip():
            st.markdown("""
            <div class="result-error">
                <h4>Validation Error</h4>
                <p>Please enter your education level</p>
            </div>
            """, unsafe_allow_html=True)
            return

        if not employee_status.strip():
            st.markdown("""
            <div class="result-error">
                <h4>Validation Error</h4>
                <p>Please enter your employment status</p>
            </div>
            """, unsafe_allow_html=True)
            return

        user_input = {
            'name': name,
            'Gender': gender,
            'Age': age,
            'Marital_Status': marital_status,
            'Dependents': dependents,
            'Education': education if education in ['Graduate', 'Undergraduate', 'High School'] else 'Graduate',
            'Employment_Status': employee_status if employee_status in ['Employed', 'Self-Employed', 'Unemployed'] else 'Employed',
            'Residential_Status': resident_status,
            'Annual_Income': annual_income,
            'Monthly_Income': monthly_income,
            'Credit_Score': credit_score,
            'Existing_Loans': existing_loans,
            'Total_Existing_Loan_Amount': existing_loan_amount,
            'Loan_Amount_Requested': requested_amount,
            'Loan_Term': loan_terms,
            'Loan_Purpose': loan_purpose,
            'Bank_Account_History': bank_account_history
        }

        with st.spinner("Processing your loan application..."):
            prev_suggestion = get_previous_suggestion(name)
            result = assess_and_suggest(
                user_input, clf_model, clf_scaler, hybrid_model,
                cap_at_requested=True, round_to=1000,
                prev_suggested_amount=prev_suggestion
            )

        save_to_database(user_input, result)

        if result["final_eligibility"] == "Eligible":
            st.markdown(f"""
            <div class="result-success">
                <h3>Loan Application Approved!</h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Combined message with suggestion in same box
            if result["suggested_amount"]:
                st.markdown(f"""
                <div class="result-combined">
                    <div class="combined-content">
                        <div class="combined-left">
                            <h3>Loan Application Not Approved</h3>
                        </div>
                        <div class="combined-right">
                            <h4>We can offer you:</h4>
                            <p class="amount">{result['suggested_amount']:,.0f}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-error">
                    <h3>Loan Application Not Approved</h3>
                </div>
                """, unsafe_allow_html=True)

        st.session_state.eligibility_checked = True

    if reset_form:
        st.session_state.eligibility_checked = False
        st.rerun()


if __name__ == "__main__":
    main()
