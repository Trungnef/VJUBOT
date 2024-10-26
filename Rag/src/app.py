import os

# Disable tokenizer parallelism
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from src.base.llm_model import get_hf_llm
from src.rag.main import build_rag_chain, InputQA, OutputQA
from fastapi import UploadFile, File, HTTPException
from src.rag.file_loader import Loader
from src.rag.vectorstore import VectorDB
import shutil

import logging

# Biến toàn cục để lưu trữ RAG chain
global genai_chain

# Initialize the language model with specific parameters
generation_kwargs = {
    "max_new_tokens": 768,
    "do_sample": True,
    "top_p": 0.95,
    "top_k": 40,
    "temperature": 0.01,
    "repetition_penalty": 1.05
}
llm = get_hf_llm(model_kwargs=generation_kwargs)
# llm = get_hf_llm(temperature=0.1)

# Specify the directory for generative AI documents
genai_docs = "./data_source/generative_ai"

# Build the RAG chain using the specified documents
genai_chain = build_rag_chain(llm, data_dir=genai_docs, data_type="pdf")

# Create a FastAPI application instance
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using Langchain's Runnable interfaces"
)

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Define the health check endpoint
@app.get("/check")
async def check():
    return {"status": "ok"}

# Define the generative AI endpoint
@app.post("/generative_ai", response_model=OutputQA)
async def generative_ai(inputs: InputQA):
    # Invoke the RAG chain and get the ranked answer
    answer = genai_chain.invoke(inputs.question)
    return {"answer": answer}

# Add routes to the application for Langserve
add_routes(app,
           genai_chain,
           playground_type="default",
           path="/generative_ai")

def update_genai_chain():
    """Update genai_chain with new data."""
    global genai_chain
    genai_docs = "./data_source/generative_ai"  # Path to generative AI documents
    # Rebuild the RAG chain
    try:
        print("Updating RAG chain...")
        genai_chain = build_rag_chain(llm, data_dir=genai_docs, data_type="pdf")
        
        # Log the documents loaded after updating the chain
        doc_list = os.listdir(genai_docs)
        print(f"Documents loaded: {doc_list}")
        
        # If using VectorDB, print retriever details to confirm update
        retriever = VectorDB(documents=Loader(file_type="pdf").load_dir(genai_docs, workers=2)).get_retriever()
        print(f"Updated retriever contains {len(retriever.get_relevant_documents('test'))} documents.")
        
    except Exception as e:
        logging.error(f"Error while updating RAG chain: {e}")
        
        
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join("./data_source/generative_ai/", file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Cập nhật genai_chain sau
        update_genai_chain()

        return {"message": "File uploaded successfully and RAG updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")    
    
@app.get("/files")
async def get_files():
    file_list = os.listdir("./data_source/generative_ai/")
    return file_list

@app.delete("/delete/{filename}")
async def delete_file(filename: str):
    file_path = os.path.join("./data_source/generative_ai/", filename)
    try:
        # Check if file exists
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {filename}")
            
            # Update RAG chain after file deletion
            update_genai_chain()

            return {"message": "File deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="File not found")
    
    except Exception as e:
        logging.error(f"Error while deleting file: {e}")
        raise HTTPException(status_code=500, detail=f"Delete failed: {e}")

@app.get("/test_retrieval")
async def test_retrieval():
    # Test with a sample query
    sample_query = "What is Generative AI?"
    result = genai_chain.invoke(sample_query)
    return {"result": result}
