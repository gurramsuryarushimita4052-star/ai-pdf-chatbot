
import streamlit as st
from pypdf import PdfReader
import re

st.set_page_config(page_title="AI PDF Chatbot", page_icon="📚")

st.title("📚 AI PDF Chatbot")
st.write("Upload a PDF and ask questions about its content.")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

def get_words(text):
    return set(re.findall(r"\b[a-zA-Z0-9]+\b", text.lower()))

if uploaded_file is not None:
    try:
        reader = PdfReader(uploaded_file)
        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            if text.strip():
                pages.append({
                    "page": page_number,
                    "text": text
                })

        if not pages:
            st.error("PDF lo readable text kanipinchaledhu.")
        else:
            st.success("PDF successfully upload ayyindhi!")

            question = st.text_input(
                "Mee question ikkada type cheyyandi"
            )

            if question:
                question_words = get_words(question)
                results = []

                for item in pages:
                    page_words = get_words(item["text"])
                    score = len(question_words & page_words)

                    if score > 0:
                        results.append((score, item))

                results.sort(
                    key=lambda result: result[0],
                    reverse=True
                )

                if results:
                    st.subheader("Relevant PDF Information")

                    for score, item in results[:3]:
                        st.write(f"Page {item['page']}")
                        st.write(item["text"][:3000])
                        st.divider()
                else:
                    st.warning(
                        "Matching information dorakaledhu. "
                        "Question ni vere words tho adigi choodandi."
                    )

    except Exception as error:
        st.error(f"PDF read cheyyadam lo problem: {error}")