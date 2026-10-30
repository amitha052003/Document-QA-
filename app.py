import streamlit as st

from pdf_processor import extract_pages, create_chunks
from safety import validate_question, check_prompt_injection
from rag import retrieve_relevant_chunks, generate_answer
from logger import log_question, log_success, log_error


st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="📚",
    layout="wide"
)


st.title("📚 Enterprise Knowledge Assistant")

st.write(
    "Upload an internal PDF document and ask questions "
    "based on its content."
)

st.divider()


# Store document information in session
if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "document_name" not in st.session_state:
    st.session_state.document_name = ""


# -----------------------------------
# 1. Upload Document
# -----------------------------------

st.subheader("1. Upload Document")

uploaded_file = st.file_uploader(
    "Choose a PDF document",
    type=["pdf"]
)


if uploaded_file:

    try:

        pages = extract_pages(uploaded_file)

        chunks = create_chunks(pages)

        st.session_state.chunks = chunks
        st.session_state.document_name = uploaded_file.name

        st.success(
            f"Document processed successfully! "
            f"{len(pages)} pages and "
            f"{len(chunks)} text chunks extracted."
        )

        with st.expander("Document Details"):

            st.write(
                f"**File:** {uploaded_file.name}"
            )

            st.write(
                f"**Pages:** {len(pages)}"
            )

            st.write(
                f"**Text Chunks:** {len(chunks)}"
            )

    except Exception as e:

        log_error(str(e))

        st.error(
            "Unable to process the PDF. "
            "Please make sure it is a valid PDF."
        )


# -----------------------------------
# 2. Ask Question
# -----------------------------------

st.subheader("2. Ask a Question")

question = st.text_input(
    "Enter your question",
    placeholder="Example: What is the company's leave policy?"
)


if st.button("🔍 Ask Question", type="primary"):

    valid, message = validate_question(question)

    if not valid:

        st.warning(message)

    elif not check_prompt_injection(question):

        st.warning(
            "I can only answer questions using "
            "the provided document."
        )

    elif not st.session_state.chunks:

        st.warning(
            "Please upload a PDF document first."
        )

    else:

        try:

            log_question(question)

            with st.spinner(
                "Searching the document and generating answer..."
            ):

                relevant_chunks = retrieve_relevant_chunks(
                    question,
                    st.session_state.chunks,
                    top_k=5
                )

                answer, sources = generate_answer(
                    question,
                    relevant_chunks,
                    st.session_state.document_name
                )

            st.subheader("Answer")

            st.write(answer)

            if sources:

                st.subheader("📄 Sources")

                for source in sources:

                    st.write(
                        f"• {source}"
                    )

            log_success(
                question,
                sources
            )

        except Exception as e:

            log_error(str(e))

            st.error(
                "Something went wrong while processing "
                "your question. Please check your Azure "
                "configuration."
            )