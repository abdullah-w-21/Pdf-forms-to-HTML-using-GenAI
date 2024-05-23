from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import streamlit as st
from pdfminer.high_level import extract_text

# Load environment variables
load_dotenv()

# Function to extract text from the uploaded PDF file
def load_pdf(file):
    try:
        pdf_text = extract_text(file)
        return pdf_text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

# Function to generate interactive HTML form from parsed PDF text
def pdf_to_llm(pdf_text):
    answer_prompt = PromptTemplate.from_template(
        "Given the following parsed pdf form, generate a proper interactive HTML form:\n\nParsed PDF Form: {pdf_text}\n\n Your job is to output the whole complete html, only provide output of the converted html nothing more, make sure the whole complete html is provided."
    )
    llm_model = ChatGroq(model="mixtral-8x7b-32768", api_key=os.getenv("GROQ_API_KEY"))
    llm = LLMChain(llm=llm_model, prompt=answer_prompt)

    try:
        # Debugging: log the prompt being sent
        st.text("Sending the following prompt to the LLM:")
        st.text(answer_prompt.format(pdf_text=pdf_text))

        # Run the model
        response = llm.run({"pdf_text": pdf_text})

        # Debugging: log the entire response
        st.text("Received the following response from the LLM:")
        st.text(response)  # Use st.text to print the entire response

        # Assume the response is plain HTML
        return response
    except Exception as e:
        st.error(f"Error generating interactive form: {e}")
        return None

# Main function for Streamlit app
def main():
    st.title("PDF to Interactive Form Converter")

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        pdf_text = load_pdf(uploaded_file)
        if pdf_text:
            st.subheader("Uploaded PDF file content:")
            st.text(pdf_text)

            # Generate interactive form
            interactive_form = pdf_to_llm(pdf_text)
            if interactive_form:
                st.subheader("Interactive HTML Form:")
                st.markdown(interactive_form, unsafe_allow_html=True)

                # Download option
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
