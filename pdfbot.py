import pytesseract
from PIL import Image
import fitz
import streamlit as st
import io
import google.generativeai as genai
import os
from io import BytesIO
import base64

os.environ["GEMINI_API_KEY"] = "AIzaSyBz3UYxuzB7qhwx9d74AnYpRumsmeK5AVM" 
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-2.0-pro-exp-02-05")

# Preeti-to-Unicode conversion function
unicodeatoz = ["ब", "द", "अ", "म", "भ", "ा", "न", "ज", "ष्", "व", "प", "ि", "फ", "ल", "य", "उ", "त्र", "च", "क", "त", "ग", "ख", "ध", "ह", "थ", "श"]
unicodeAtoZ = ["ब्", "ध", "ऋ", "म्", "भ्", "ँ", "न्", "ज्", "क्ष्", "व्", "प्", "ी", "ः", "ल्", "इ", "ए", "त्त", "च्", "क्", "त्", "ग्", "ख्", "ध्", "ह्", "थ्", "श्"]
unicode0to9 = ["ण्", "ज्ञ", "द्द", "घ", "द्ध", "छ", "ट", "ठ", "ड", "ढ"]
symbolsDict = {
    "~": "ञ्", "`": "ञ", "!": "१", "@": "२", "#": "३", "$": "४", "%": "५", "^": "६", "&": "७", "*": "८",
    "(": "९", ")": "०", "-": "(", "_": ")", "+": "ं", "[": "ृ", "{": "र्", "]": "े", "}": "ै", "\\": "्",
    "|": "्र", ";": "स", ":": "स्", "'": "ु", "\"": "ू", ",": ",", "<": "?", ".": "।", ">": "श्र", "/": "र",
    "?": "रु", "=": ".", "ˆ": "फ्", "Î": "ङ्ख", "å": "द्व", "÷": "/"
}

def normalizePreeti(preetitxt):
    normalized = ''
    previoussymbol = ''
    preetitxt = preetitxt.replace('qm', 's|').replace('f]', 'ो').replace('km', 'फ').replace('0f', 'ण')
    preetitxt = preetitxt.replace('If', 'क्ष').replace('if', 'ष').replace('cf', 'आ')
    index = -1
    while index + 1 < len(preetitxt):
        index += 1
        character = preetitxt[index]
        try:
            if preetitxt[index + 2] == '{' and (preetitxt[index + 1] == 'f' or preetitxt[index + 1] == 'ो'):
                normalized += '{' + character + preetitxt[index + 1]
                index += 2
                continue
            if preetitxt[index + 1] == '{' and character != 'f':
                normalized += '{' + character
                index += 1
                continue
        except IndexError:
            pass
        if character == 'l':
            previoussymbol = 'l'
            continue
        else:
            normalized += character + previoussymbol
            previoussymbol = ''
    return normalized

def convert(preeti):
    converted = ''
    normalizedpreeti = normalizePreeti(preeti)
    for character in normalizedpreeti:
        try:
            if 'a' <= character <= 'z':
                converted += unicodeatoz[ord(character) - ord('a')]
            elif 'A' <= character <= 'Z':
                converted += unicodeAtoZ[ord(character) - ord('A')]
            elif '0' <= character <= '9':
                converted += unicode0to9[ord(character) - ord('0')]
            else:
                converted += symbolsDict.get(character, character)
        except KeyError:
            converted += character
    return converted

def extract_text_from_image(pdf_document): 
    """Extracts text from images in the PDF using Tesseract OCR."""
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        text += pytesseract.image_to_string(img, lang='eng+nep')
    return text

def extract_text_from_pdf(uploaded_file): 
    """Extracts text from the uploaded PDF file."""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = "\n".join([page.get_text("text") for page in doc])
    return text

def download_button(converted_text):
    """Generates a download button for the converted text."""
    towrite = BytesIO()
    towrite.write(converted_text.encode('utf-8'))
    towrite.seek(0) 
    b64 = base64.b64encode(towrite.read()).decode()
    file_name = "converted_text.txt"
    md= f"""
    <a href="data:file/txt;base64,{b64}" download="{file_name}">Download Converted Text</a>
    """
    st.markdown(md, unsafe_allow_html=True)

# --- Streamlit UI ---
st.set_page_config(page_title="Nepali PDF Chatbot", page_icon="🇳🇵")

st.title("🇳🇵 Nepali PDF Chatbot (Preeti Supported)")
st.markdown("Upload a Nepali PDF (Preeti font or standard) and ask questions about its content.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    status_text = "Processing PDF..."
    status_bar = st.status(status_text)
    unicode_text = ""
    try:
        with fitz.open(uploaded_file) as doc:
            text = ""
            # text = extract_text_from_pdf(uploaded_file)
            if any(page.get_text("text").strip() for page in doc):
                text = extract_text_from_pdf(uploaded_file)
            else:
                text = extract_text_from_image(doc)
                
        # Convert extracted text from Preeti to Unicode
        unicode_text = convert(text)
        status_bar.update(label="PDF Processing Complete!", state="complete", expanded=False)

        with st.expander("Show Extracted & Converted Text", expanded=False):
            st.text_area("Nepali Unicode Text", unicode_text.encode('utf-8').decode('utf-8'), height=300)
            download_button(unicode_text)

        # Chat interface
        st.markdown("---")
        st.subheader("Ask me anything about the PDF")
        question = st.text_input("Your question:")

        col1, col2 = st.columns([1, 2])
        with col1:
            language = st.radio("Response Language:", ("English", "Nepali"))
        with col2:
            if st.button("Get Answer", use_container_width=True):
                if question:
                    lang_code = "in English" if language == "English" else "in Nepali"
                    full_prompt = f"Context from the PDF:\n{unicode_text}\n\nAnswer the following question {lang_code}:\n{question}"

                    with st.spinner("Generating answer..."):
                        try:
                            chat_session = model.start_chat(history=[])
                            response = chat_session.send_message(full_prompt)
                            st.markdown(f"**Answer ({language}):**")
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Error querying the model: {e}")
                else:
                    st.warning("Please enter a question.")

    except Exception as pdf_error:
        status_bar.update(label="PDF Processing Error!", state="error", expanded=True)
        st.error(f"Error processing PDF: {pdf_error}")
        st.error("Please ensure the PDF is not corrupted and try again.")