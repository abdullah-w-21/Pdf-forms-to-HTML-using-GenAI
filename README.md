# Pdf-forms-to-HTML-using-GenAI
A simple tool with streamlit interface made to convert PDF forms to HTML forms using LLM (Mixtral)


# PDF to Interactive Form Converter

This project provides a Streamlit application that converts PDF files into interactive HTML forms using a language model.

## Overview

The application allows users to upload a PDF file, extracts the text from the PDF, and then uses a language model to generate an interactive HTML form based on the extracted text. The generated HTML form can be viewed directly in the application and downloaded for further use.

## Setup

To run this application, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/pdf-to-interactive-form.git
   cd pdf-to-interactive-form
    ```
2. Install Dependencies

Make sure you have Python installed, then install the required packages using pip

3. Set Up Environment Variables

Create a .env file in the root directory of the project and add your API key for the language model:

```bash
GROQ_API_KEY=your_groq_api_key
 ```

4. Run the Application

Start the Streamlit application by running:

```bash
streamlit run app.py
```

## Code Explanation

## Importing Libraries

```bash
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import streamlit as st
from pdfminer.high_level import extract_text

```
- langchain_groq: For interacting with the language model.
- dotenv: For loading environment variables.
- streamlit: For creating the web application.
- pdfminer: For extracting text from PDF files.

## Loading Environment Variables

```bash
load_dotenv()

```

Loads the environment variables from a .env file.


## Function to Extract Text from PDF

```bash
def load_pdf(file):
    try:
        pdf_text = extract_text(file)
        return pdf_text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

```

This function extracts text from the uploaded PDF file using pdfminer.


## Function to Generate Interactive HTML Form

```bash
def pdf_to_llm(pdf_text):
    answer_prompt = PromptTemplate.from_template(
        "Given the following parsed pdf form, generate a proper interactive HTML form:\n\nParsed PDF Form: {pdf_text}\n\n Your job is to output the whole complete html, only provide output of the converted html nothing more, make sure the whole complete html is provided."
    )
    llm_model = ChatGroq(model="mixtral-8x7b-32768", api_key=os.getenv("GROQ_API_KEY"))
    llm = LLMChain(llm=llm_model, prompt=answer_prompt)

    try:
        st.text("Sending the following prompt to the LLM:")
        st.text(answer_prompt.format(pdf_text=pdf_text))

        response = llm.run({"pdf_text": pdf_text})

        st.text("Received the following response from the LLM:")
        st.text(response)

        return response
    except Exception as e:
        st.error(f"Error generating interactive form: {e}")
        return None

```
This function generates an interactive HTML form from the extracted PDF text using a language model.

## Main Function for Streamlit App

```bash
def main():
    st.title("PDF to Interactive Form Converter")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        pdf_text = load_pdf(uploaded_file)
        if pdf_text:
            st.subheader("Uploaded PDF file content:")
            st.text(pdf_text)

            interactive_form = pdf_to_llm(pdf_text)
            if interactive_form:
                st.subheader("Interactive HTML Form:")
                st.markdown(interactive_form, unsafe_allow_html=True)

                st.markdown("---")
                st.subheader("Download Interactive Form")
                st.download_button(
                    label="Download Form",
                    data=interactive_form.encode("utf-8"),
                    file_name="interactive_form.html",
                    mime="text/html",
                )

if __name__ == "__main__":
    main()

```

The main function sets up the Streamlit application, handles file uploads, displays the extracted PDF text, generates the interactive form, and provides an option to download the form.

## Requirements

Create a requirements.txt file with the following content:

```bash
langchain_groq
python-dotenv
streamlit
pdfminer.six

```

This file lists all the dependencies required to run the application.






***Note: This code contains alot of unneccessary print statements in streamlit this was just for debugging i was lazy and i didnt remove them while uploading to github, u may remove them:). Any constructive feedback regarding this is appreciated :). This is a simpler version currently working on a better version using llama-parser to parse the pdf and using multiple chains for the conversion to get a more better result any reccommendations for better approach is appreciated.***













