# streamlit_app.py
import streamlit as st
from main import ingest_document, answer_question, online_search

# ------------------------------
# Streamlit App Config
# ------------------------------
st.set_page_config(page_title="Concert Tour Helper", layout="centered")

st.title("Concert Tour Helper")
st.subheader("Choose your mode:")

mode = st.radio("Select an option:", ["Ask a question", "Add a document", "Search artist online"])
st.markdown("---")

# ------------------------------
# Ask a question mode
# ------------------------------
if mode == "Ask a question":
    query = st.text_input("Ask something about concert tours:")
    if st.button("Submit Question") and query:
        answer = answer_question(query)
        if answer:
            st.success(answer)
        else:
            st.warning("No local answer found. Searching online...")
            web_answer = online_search(query)
            st.success(web_answer)
    elif st.button("Submit Question"):
        st.error("Please enter a question.")

# ------------------------------
# Add document mode
# ------------------------------
elif mode == "Add a document":
    uploaded_file = st.file_uploader(
        "Upload a concert tour document (.txt, .pdf, .docx, .json, .csv)",
        type=["txt", "pdf", "docx", "json", "csv"]
    )
    if uploaded_file and st.button("Ingest Document"):
        file_bytes = uploaded_file.read()
        result = ingest_document(file_bytes, uploaded_file.name)
        st.success("Document successfully ingested!")
        if isinstance(result, dict):
            st.info(f"Summary:\n{result.get('summary', '')}")
            st.write(f"Metadata:\n{result.get('metadata', {})}")
        else:
            st.info(f"Summary:\n{result}")

# ------------------------------
# Search artist online mode
# ------------------------------
elif mode == "Search artist online":
    artist = st.text_input("Enter a musician or band name:")
    if st.button("Search Artist") and artist:
        result = online_search(artist)
        st.json(result)
    elif st.button("Search Artist"):
        st.error("Please enter an artist name.")
