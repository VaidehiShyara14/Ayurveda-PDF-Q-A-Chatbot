import os
from dotenv import load_dotenv
from io import BytesIO
import tempfile

from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings  
from langchain_groq import ChatGroq
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA


#Load API key from .env
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

#Load Groq LLM
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-8b-8192"
)

 #Create retriever from uploaded PDF 
def create_retriever_from_pdf(pdf_bytes):
    # Save PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_bytes)
        tmp_path = tmp_file.name

    # Load and split PDF
    docs = PyMuPDFLoader(tmp_path).load()
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(docs)

    # Create vectorstore
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(chunks, embeddings)
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    return retriever


def generate_answer(question, retriever):
    custom_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an expert Ayurvedic assistant trained on classical and modern Ayurvedic texts.

Answer the following question based strictly on the provided context from the uploaded PDF.

If the answer is found in the text, answer clearly and concisely using plain English. 
If a classical Sanskrit reference is included, quote it accurately and explain it briefly.

If the answer is not present in the context, respond with: 
"I couldn’t find a specific answer to your question in the provided document."

Use this structure:
Answer: <your answer>
Sanskrit Reference: <if applicable>
Source Summary: <brief source location or context>

Context:
{context}

Question: {question}
"""
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": custom_prompt}
    )

    result = qa.invoke({"query": question}) 
    return result["result"]




