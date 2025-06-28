import streamlit as st
import requests

# Backend URL
API_URL = "http://localhost:40000"

# Page Config
st.set_page_config(page_title="🧠 Ayurveda PDF QA", layout="centered")


# Beautiful Header

st.markdown("""
    <div style='text-align: center; padding: 10px 0 20px 0;'>
        <h1 style='font-size: 2.5em; color: #2c6e49;'>🌿 Ayurveda PDF Q&A Chatbot</h1>
        <p style='font-size: 1.1em; color: #555;'>Ask questions from your uploaded Ayurveda PDFs.</p>
    </div>
""", unsafe_allow_html=True)

#  Session State
if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False


# 📄 PDF Upload

st.subheader("📤 Upload Ayurveda PDF")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    with st.spinner("📚 Indexing the document..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        try:
            response = requests.post(f"{API_URL}/upload/", files=files)
            result = response.json()
            if response.status_code == 200:
                st.success(result.get("message", "✅ PDF uploaded and indexed."))
                st.session_state.pdf_uploaded = True
            else:
                st.error(result.get("error", "❌ Upload failed."))
                st.session_state.pdf_uploaded = False
        except requests.exceptions.ConnectionError:
            st.error("🚫 Cannot connect to FastAPI backend. Is it running on port 40000?")
            st.stop()


# Ask a Question

if st.session_state.pdf_uploaded:
    st.subheader("💬 Ask a Question")

    with st.form("qa_form"):
        question = st.text_input("Type your question:")
        submitted = st.form_submit_button("🔍 Get Answer")

        if submitted and question:
            with st.spinner("🤖 Thinking..."):
                try:
                    response = requests.post(f"{API_URL}/ask/", json={"question": question})
                    result = response.json()

                    if "answer" in result:
                        with st.expander("📜 View Answer", expanded=True):
                            st.markdown(f"**Answer:**\n{result['answer']}")
                    else:
                        st.warning(result.get("error", "❌ No answer found."))

                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend.")


