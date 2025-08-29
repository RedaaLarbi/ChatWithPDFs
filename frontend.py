import streamlit as st
from backend import comp_process


def frontend():

    #sreamlit UI
    st.set_page_config(page_title="Chat with multiple pdf files!", layout="wide")
    st.title("Chat with Multiple :red[PDF Files]!")
    question = st.text_input("Ask questions Below: ")
   
    
    with st.sidebar:
        st.image("image.png")
        
        api_key = st.text_input("Enter apikey", placeholder="Enter openAI Key", type="password")
        
        st.subheader("Upload PDFs Here")
        
        pdfs = st.file_uploader("Upload PDF Files", type="pdf", accept_multiple_files=True) 
        
        st.button("Process")
    

    if st.button("Get Answer"):
        if not api_key:
            st.error("Please enter your OpenAI API key.")
        elif not pdfs:
            st.error("Please upload at least one PDF.")
        elif not question.strip():
            st.error("Please type a question.")
        else:
            with st.spinner("Processing..."):
                try:
                    # Convert UploadedFile objects to file paths
                    file_paths = []
                    for pdf in pdfs:
                        temp_path = f"/tmp/{pdf.name}"
                        with open(temp_path, "wb") as f:
                            f.write(pdf.getbuffer())
                        file_paths.append(temp_path)

                    ans = comp_process(api_key, file_paths, question)
                    st.success(ans)
                except Exception as e:
                    st.error(f"Error: {e}")


if __name__ == "__main__":
    frontend()