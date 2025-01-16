import streamlit as st
import PyPDF2
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk

# Download NLTK stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def preprocess_text(text):
    """Preprocesses the text by converting to lowercase and removing non-alphanumeric characters."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def remove_stopwords(text):
    """Removes stop words from the text."""
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

def generate_wordcloud(text):
    """Generates and displays a word cloud from the text."""
    wordcloud = WordCloud(width=800, height=400, max_words=500, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

def main():
    st.title("PDF WordCloud Generator")
    st.write("Upload a PDF file, and we'll create a word cloud of the most frequent words (excluding stop words).")

    pdf_file = st.file_uploader("Upload PDF", type="pdf")

    if pdf_file is not None:
        # Extract text from the uploaded PDF
        with st.spinner("Extracting text from PDF..."):
            extracted_text = extract_text_from_pdf(pdf_file)

        # Preprocess the text
        preprocessed_text = preprocess_text(extracted_text)

        # Remove stop words
        filtered_text = remove_stopwords(preprocessed_text)

        # Generate and display the word cloud
        st.subheader("Word Cloud")
        generate_wordcloud(filtered_text)

if __name__ == "__main__":
    main()
