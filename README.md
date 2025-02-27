# Nepali PDF Chatbot (Preeti Supported) 🇳🇵

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-orange?logo=streamlit)](https://streamlit.io/) [![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](https://www.python.org/)

This Streamlit application is designed to process Nepali PDF documents, especially those using the Preeti font, and allows users to ask questions about the content using a chatbot powered by Google's Gemini AI model.

## ✨ Key Features

*   **Nepali PDF Processing:** Handles PDF documents written in Nepali language.
*   **Preeti Font Support:** Includes a built-in converter to handle PDFs encoded in the Preeti font, converting it to Unicode for accurate text extraction and processing.
*   **Text Extraction:** Extracts text from both text-based PDFs and image-based PDFs (using OCR with Tesseract).
*   **Chatbot Functionality:** Integrates with Google Gemini AI to provide conversational answers to questions about the PDF content in both English and Nepali.
*   **User-Friendly Interface:** Built with Streamlit for an intuitive and easy-to-use web interface.
*   **Download Converted Text:** Option to download the extracted and Preeti-converted text as a `.txt` file.

## 🚀 How to Use

Follow these steps to run the Nepali PDF Chatbot application:

### Prerequisites

1.  **Python:** Ensure you have Python 3.9 or later installed on your system. You can download it from [python.org](https://www.python.org/).
2.  **Libraries:** Install the required Python libraries. It is recommended to create a virtual environment to manage dependencies.

    ```bash
    pip install streamlit pytesseract pillow PyMuPDF google-generativeai
    ```

    *   **Tesseract OCR:**  You need to have Tesseract OCR engine installed separately on your system.
        *   **Windows:** Download from [Tesseract OCR website](https://tesseract-ocr.github.io/tessdoc/tesseract4-installer.html). Make sure to add Tesseract to your system's PATH environment variable.
        *   **macOS:**  Install using Homebrew: `brew install tesseract`
        *   **Linux (Ubuntu):** `sudo apt install tesseract-ocr`
    *   **Google Generative AI API Key:** You need a Google Generative AI API key to use the Gemini model.
        1.  Go to [Google AI Studio](https://makersuite.google.com/app/apikey) and create a project if you don't have one.
        2.  Generate an API key.
        3.  **Important:** For security, it is highly recommended to set your API key as a Streamlit secret or environment variable instead of hardcoding it directly in the script.

### Installation and Running

1.  **Clone the repository:** (If you are creating a repository for this code)

    ```bash
    git clone [https://github.com/stha-sanket/PDF-Query-Bot.git]
    ```

2.  **Set up API Key:**
    *   **Recommended (Streamlit Secrets):**  Create a `.streamlit/secrets.toml` file in your project directory (or within your Streamlit app's directory if deploying). Add your API key like this:

        ```toml
        GEMINI_API_KEY = "YOUR_API_KEY_HERE" # enter your api key in this field donot copy mine
        ```
        Then, in your Python code, access it using: `os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]`

    *   **Environment Variable (Less Secure):** Set an environment variable named `GEMINI_API_KEY` with your API key value in your operating system.

3.  **Run the Streamlit app:**

    ```bash
    streamlit run pdfbot.py  # Replace your_script_name.py with the name of your Python file
    ```

4.  **Access the App:** Open your web browser and go to the URL displayed in the terminal (usually `http://localhost:8501`).

### Using the Application

1.  **Upload PDF:** Click on the "Browse files" button or drag and drop a Nepali PDF file into the file uploader widget.
2.  **Wait for Processing:** The application will process the PDF, extract text, and convert Preeti font if necessary. A status message will indicate the progress.
3.  **View Extracted Text (Optional):** Expand the "Show Extracted & Converted Text" section to review the extracted Unicode text and download it as a `.txt` file.
4.  **Ask Questions:** In the "Ask me anything about the PDF" section, type your question in the text input field.
5.  **Choose Language:** Select your desired response language (English or Nepali) using the radio buttons.
6.  **Get Answer:** Click the "Get Answer" button. The Gemini AI model will generate an answer based on the PDF content and display it below.

## ⚙️ Preeti Font Conversion

This application includes a custom function to convert text extracted from PDFs using the Preeti font into Unicode. This ensures that Nepali text is displayed correctly and can be processed by the chatbot. The conversion is based on mapping Preeti characters to their Unicode equivalents using predefined dictionaries.

## 🤖 Gemini AI Integration

The chatbot functionality is powered by Google's Gemini Pro AI model.  The application sends a prompt to Gemini, including the extracted text from the PDF as context and the user's question. Gemini then generates a response based on this information, providing answers related to the PDF content.

## ⚠️ Limitations and Future Improvements

*   **OCR Accuracy:**  OCR accuracy for image-based PDFs, especially with complex layouts or low-resolution images, may vary.
*   **Complex Preeti Fonts:** The Preeti conversion might not cover all variations or very stylized versions of the Preeti font.
*   **Context Window:**  The amount of PDF text that can be effectively used as context for the Gemini model is limited by the model's context window. For very large PDFs, the chatbot might not have access to the entire document's content at once.
*   **Future improvements could include:**
    *   More robust Preeti font handling.
    *   Improved error handling and user feedback.
    *   Summarization features for large PDFs.
    *   More advanced prompt engineering for better chatbot responses.

---

**Made with using Streamlit, Python, and Google Gemini AI.**
