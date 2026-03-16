import streamlit as st
import sys
import os
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.agent.main_agent import run_main_agent

st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# LIGHT/DARK SAFE CSS
# -----------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1rem;
    max-width: 1100px;
}

[data-testid="stSidebar"] {
    min-width: 280px;
    max-width: 280px;
}

.app-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}

.app-subtitle {
    font-size: 0.9rem;
    opacity: 0.75;
    margin-bottom: 1rem;
}

.section-label {
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 0.4rem;
    margin-top: 0.4rem;
}

.risk-box {
    border: 1px solid rgba(128,128,128,0.25);
    border-radius: 12px;
    padding: 10px 14px;
    margin-top: 8px;
    background: rgba(128,128,128,0.06);
}

.small-muted {
    font-size: 0.85rem;
    opacity: 0.7;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# BACKEND FUNCTION
# -----------------------------
def get_backend_response(user_input: str, uploaded_file=None) -> dict:
    file_path = None

    if uploaded_file is not None:
        suffix = ""
        if uploaded_file.name:
            _, suffix = os.path.splitext(uploaded_file.name)

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getvalue())
            file_path = tmp.name

    return run_main_agent(user_input, file_path)
# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown('<div class="app-title">🛡️ FraudGuard AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-subtitle">Fraud detection, OCR, RAG, sanctions, and image authenticity.</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="section-label">Upload file</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload a file",
        type=["png", "jpg", "jpeg", "pdf", "csv"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        st.success(f"Attached: {uploaded_file.name}")
    else:
        st.markdown('<div class="small-muted">No file attached</div>', unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="section-label">Actions</div>', unsafe_allow_html=True)

    if st.button("New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# MAIN HEADER
# -----------------------------
st.title("FraudGuard AI")
st.caption("Ask about suspicious transactions, AML rules, sanctions, OCR documents.")

# -----------------------------
# CHAT HISTORY
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

       
# -----------------------------
# CHAT INPUT
# -----------------------------
user_input = st.chat_input("Message FraudGuard AI...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    result = get_backend_response(user_input, uploaded_file)

    with st.chat_message("assistant"):
        st.markdown(result["reply"])
        

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["reply"],
        "risk": result["risk"],
        "score": result["score"]
    })