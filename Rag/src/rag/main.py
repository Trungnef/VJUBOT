from pydantic import BaseModel, Field
from src.rag.file_loader import Loader
from src.rag.vectorstore import VectorDB
from src.rag.offline_rag import Offline_RAG
from src.rag.reranker import CohereReranker

# Input and Output models for QA
class InputQA(BaseModel):
    question: str = Field(..., title="Question to ask the model")

class OutputQA(BaseModel):
    answer: str = Field(..., title="Answer from the model")

# Function to build RAG chain
def build_rag_chain(llm, data_dir, data_type, use_reranker=True):
    doc_loaded = Loader(file_type=data_type).load_dir(data_dir, workers=2)
    retriever = VectorDB(documents=doc_loaded).get_retriever()
    if use_reranker:
        reranker = CohereReranker()  # Initialize the reranker
        rag_chain = Offline_RAG(llm).get_chain(retriever, reranker=reranker)  # Pass the reranker to get_chain
    else:
        rag_chain = Offline_RAG(llm).get_chain(retriever)

    return rag_chain
