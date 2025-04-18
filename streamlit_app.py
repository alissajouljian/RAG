import streamlit as st
from main import ingest_document, answer_question, online_search

st.set_page_config(page_title="Concert Tour Helper ", layout="centered")

st.title("Concert Tour Helper )")
st.subheader("Choose your mode:")

mode = st.radio("Select an option:", ["Ask a question", "Add a document", "Search artist online"])

st.markdown("---")  

if mode == "Ask a question":
    query = st.text_input("Ask something about concert tours:")
    if st.button("Submit Question"):
        if query:
            answer = answer_question(query)
            if answer:
                st.success(answer)
            else:
                st.warning("No local answer found. Searching online...")
                web_answer = online_search(query)
                st.success(web_answer)
        else:
            st.error("Please enter a question.")

elif mode == "Add a document":
    uploaded_file = st.file_uploader("Upload a concert tour document (.txt format)", type=["txt"])
    if uploaded_file and st.button("Ingest Document"):
        file_bytes = uploaded_file.read()
        result = ingest_document(file_bytes, uploaded_file.name)

        st.success("Document successfully ingested!")
        st.info(f"Summary:\n{result}")

elif mode == "Search artist online":
    artist = st.text_input("Enter a musician or band name:")
    if st.button("Search Artist"):
        if artist:
            result = online_search(artist)
            st.success(result)
        else:
            st.error("Please enter an artist name.")
