import streamlit as st
import fitz  # pip install PyMuPDF (use this) ;)
import base64

def pdf_to_html(pdf_file):
    doc = fitz.open(pdf_file)
    html = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        html += page.get_text("html")
    return html

def main():
    st.title('PDF to HTML Converter')

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        html_content = pdf_to_html(uploaded_file)
        st.markdown(html_content, unsafe_allow_html=True)

        # Add a download link for the HTML file
        b64 = base64.b64encode(html_content.encode()).decode()
        href = f'<a href="data:file/html;base64,{b64}" download="converted_file.html">Download HTML File</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
