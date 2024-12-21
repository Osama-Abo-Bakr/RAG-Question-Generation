import streamlit as st
from dotenv import load_dotenv
from fpdf import FPDF
import PyPDF2
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq

def get_pdf_text(upload_pdfs):    
    try:
        pdf_reader = PyPDF2.PdfReader(upload_pdfs)
        extracted_text = ''.join(page.extract_text() for page in pdf_reader.pages)
        st.info(extracted_text)
        return extracted_text
    except Exception as e:
        st.error(f"Failed to extract text from PDF: {e}")
        return None

def split_data_into_chunks(raw_text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators='\n',
        length_function=len
    )

    chunks = text_splitter.split_text(raw_text)
    return chunks


def store_chunks_vectorDB(chunks, embedding):
    vector_db = FAISS.from_documents(documents=chunks, embedding=embedding)
    return vector_db


def generate_questions(inputs):
    content = inputs['content']
    question_types = inputs['question_types']
    complexity_level = inputs['complexity_level']
    num_questions = inputs['num_questions']

    llm = ChatGroq(model='llama3-70b-8192')

    prompt = ChatPromptTemplate.from_template("""
        You are an AI designed to analyze and extract meaningful information from text documents. Your task is to read the content of a PDF document uploaded by the user and generate insightful, relevant, and clear questions based on the context.

        Context: {context}

        Here are the requirements for the questions you generate:
        1. Focus on the main ideas, key points, and important details in the content.
        2. Ensure the questions are concise and cover a range of topics from the document.
        3. Include questions of varying complexity, such as factual, analytical, and critical-thinking questions.
        4. Provide the specified types of questions (e.g., multiple-choice, short-answer, true-false, or open-ended) based on user instructions.
        5. Adjust the complexity of the questions based on the depth of the content or user requirements (basic, intermediate, or advanced level).
        6. The number of questions should vary between 5-20, depending on the length and richness of the content or user preferences.

        Input Parameters:
        - Question Types: {question_types} (e.g., multiple-choice, short-answer, true-false, open-ended)
        - Complexity Level: {complexity_level} (e.g., basic, intermediate, advanced)
        - Number of Questions: {num_questions}

        Output: A list of {question_types} questions that align with the user's requirements and the provided content.

        Please start generating the questions based on the input context and parameters.
        """)


    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retriever_chain = create_retrieval_chain(retriever, document_chain)

    with st.spinner('AI is thinking...'):
        response = retriever_chain.invoke(
            {
                'input': content,
                'complexity_level': complexity_level,
                'num_questions': num_questions,
                'question_types': question_types
            }
        )

    ai_answer = response.get('answer', 'No answer provided.')
    formatted_answer = ai_answer.replace('\n', '<br>')

    with st.chat_message("assistant"):
        st.write(formatted_answer, unsafe_allow_html=True)

    return ai_answer


def create_pdf(content, file_name="generated_questions.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Generated Questions", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    for line in content.split('\n'):
        if line.startswith("*"):
            title = line.replace("*", "").strip()
            pdf.set_font("Arial", style="B", size=14)
            pdf.cell(0, 7, txt=title, ln=True, align="L")
        else:
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 5, txt=line)
            pdf.ln(1)

    pdf.output(file_name)
    return file_name


def main():
    load_dotenv()
    st.set_page_config(page_title='Question Generator from PDF📚', page_icon='📚')

    st.title("Question Generator from PDF📚")
    st.sidebar.header("Upload PDF and Settings")

    if 'vectors' not in st.session_state:
        st.session_state.vectors = None

    upload_pdf = st.sidebar.file_uploader("Upload PDF(s) 📚", type="pdf", accept_multiple_files=False)

    st.sidebar.markdown("### Customize Question Generation")
    question_types = st.sidebar.selectbox(
        "Select Question Type:",
        ["multiple-choice", "short-answer", "true-false", "open-ended"],
        index=0
    )

    complexity_level = st.sidebar.selectbox(
        "Select Complexity Level:",
        ["basic", "intermediate", "advanced"],
        index=1
    )

    num_questions = st.sidebar.slider(
        "Number of Questions:",
        min_value=5,
        max_value=20,
        value=10,
        step=1
    )

    if upload_pdf:
        if st.sidebar.button('Process PDF📚'):
            with st.spinner('Processing PDF...'):
                st.session_state.embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
                st.session_state.raw_text = get_pdf_text(upload_pdf)
                split_chunks = split_data_into_chunks(st.session_state.raw_text)

                st.session_state.vectors = store_chunks_vectorDB(chunks=split_chunks, embedding=st.session_state.embedding)
                st.success('PDF processing complete! 🎉')

    if st.session_state.vectors:
        st.subheader("Generate Questions from Processed PDF Content")

        if st.button("Generate Questions"):
            content = " ".join([chunk.page_content for chunk in st.session_state.raw_text])
            inputs = {
                "content": content,
                "question_types": question_types,
                "complexity_level": complexity_level,
                "num_questions": num_questions
            }

            st.session_state.ai_answer = generate_questions(inputs)

        if "ai_answer" in st.session_state:
            if st.sidebar.button("Export to PDF"):
                pdf_file = create_pdf(st.session_state.ai_answer)
                with open(pdf_file, "rb") as pdf:
                    st.download_button(
                        label="Download PDF",
                        data=pdf,
                        file_name="generated_questions.pdf",
                        mime="application/pdf"
                    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.markdown("This app uses advanced AI models to process PDFs and generate insightful questions.")
    st.sidebar.title("Contact Us")
    st.sidebar.write("📧 **Email**: [osamaoabobakr12@gmail.com](mailto:osamaoabobakr12@gmail.com)")
    st.sidebar.write("📞 **Phone**: +20-1274011748")
    st.sidebar.write("🔗 **LinkedIn**: [Osama Abo Bakr](https://www.linkedin.com/in/osama-abo-bakr-293614259/)")
    st.sidebar.markdown("---")
    st.sidebar.markdown("🌐 Powered by Osama Abo-Bakr")


main()