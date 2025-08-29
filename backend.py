from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA


def comp_process(apikey, pdfs, question):
    """Process PDFs and return an answer to the question."""
    
    # 1. Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",   # or "gpt-4", "gpt-3.5-turbo"
        temperature=0,
        api_key=apikey
    )

    # 2. Load and split documents
    docs = []
    for pdf in pdfs:
        loader = PyPDFLoader(pdf)
        docs.extend(loader.load())
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    splits = text_splitter.split_documents(docs)

    # 3. Create embeddings + vectorstore
    embeddings = OpenAIEmbeddings(api_key=apikey)
    vectorstore = FAISS.from_documents(splits, embeddings)

    # 4. Build RetrievalQA chain
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )

    # 5. Run the query
    result = qa.invoke({"query": question})
    return result["result"]
    
    
