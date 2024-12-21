Here's a README file for your project:

```markdown
# Question Generator from PDF 📚

This application processes uploaded PDF documents, extracts meaningful content, and generates insightful questions using AI models. It leverages LangChain, Google Generative AI, and other advanced tools to provide high-quality, customizable questions.

## Features

- **Upload and Process PDFs**: Upload one or more PDF files, and the application processes the content to prepare it for question generation.
- **Question Generation**: Generate a set of questions based on the content of the PDF, with options to specify:
  - **Question Types**: Multiple-choice, short-answer, true-false, or open-ended.
  - **Complexity Levels**: Basic, intermediate, or advanced.
  - **Number of Questions**: Between 5 and 20 questions.
- **Export to PDF**: Save the generated questions as a downloadable PDF file.
- **Customizable Options**: Fine-tune the question generation process via the sidebar.
- **User-Friendly Interface**: Built using Streamlit for an interactive and responsive experience.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Osama-Abo-Bakr/RAG-Question-Generation.git
   cd RAG-Question-Generation
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project directory.
   - Add your Google Generative AI and other required API keys.

## Usage

1. Run the application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the provided URL (typically `http://localhost:8501`).

3. Use the sidebar to upload PDF files, select question types, complexity levels, and the number of questions.

4. Process the PDF, generate questions, and export them to a PDF file.

## Dependencies

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [LangChain](https://langchain.com/)
- [FAISS](https://faiss.ai/)
- [FPDF](http://www.fpdf.org/)
- [Google Generative AI](https://ai.google/)
- Other dependencies specified in `requirements.txt`

## Contact

For inquiries or support, please contact:

- 📧 **Email**: [osamaoabobakr12@gmail.com](mailto:osamaoabobakr12@gmail.com)
- 📞 **Phone**: +20-1274011748
- 🔗 **LinkedIn**: [Osama Abo Bakr](https://www.linkedin.com/in/osama-abo-bakr-293614259/)

---
🌐 **Powered by Osama Abo-Bakr**