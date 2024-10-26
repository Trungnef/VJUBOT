import re
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.base import BaseCallbackHandler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Custom string output parser
class Str_OutputParser(StrOutputParser):

    def __init__(self) -> None:
        super().__init__()

    def parse(self, text: str) -> str:
        return self.extract_answer(text)

    def extract_answer(self, text_response: str, pattern: str = r"Answer:\s*(.*)") -> str:
        match = re.search(pattern, text_response, re.DOTALL)
        if match:
            answer_text = match.group(1).strip()
            return answer_text
        else:
            return text_response
        
# Offline_RAG class
class Offline_RAG:
    def __init__(self, llm) -> None:
        self.llm = llm
        self.prompt = hub.pull("rlm/rag-prompt")
        self.str_parser = Str_OutputParser()

    def get_chain(self, retriever, reranker=None):
        input_data = {
            "context": retriever,
            "question": RunnablePassthrough()
        }

        callbacks = []
        if reranker:
            callbacks.append(RerankerCallback(reranker))
        
        rag_chain = (
            input_data
            | self.prompt
            | self.llm
            | self.str_parser
        )

        return rag_chain.with_config(run_config={"callbacks": callbacks})


    def format_docs(self, docs):
       return "\n\n".join(doc.page_content for doc in docs)
   
   
    
class RerankerCallback(BaseCallbackHandler):
    """Callback handler for reranking."""

    def __init__(self, reranker):
        self.reranker = reranker

    def on_retriever_end(self, documents, **kwargs):
        query = kwargs.get("query")
        if query:
            logger.info("Documents before reranking: %s", [doc.page_content[:50] for doc in documents])
            ranked_docs = self.reranker.rerank(query, documents)
            logger.info("Documents after reranking: %s", [doc.page_content[:50] for doc in ranked_docs])
            ranked_docs_with_scores = []
            with open("./src/rag/rerank_results.txt", "a") as f:
                for i, (doc, score) in enumerate(ranked_docs):
                    f.write(f"Document {i+1}: {doc.page_content[:50]} - Score: {score}\n")
                f.write("-" * 20 + "\n")


            self.callback.on_retriever_end(ranked_docs_with_scores, **kwargs)