import cohere
import os

class CohereReranker:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("Cohere API key not found. Set COHERE_API_KEY environment variable or pass api_key to the constructor.")
        self.client = cohere.Client(self.api_key)

    def rerank(self, query, docs):
        texts = [doc.page_content for doc in docs]
        response = self.client.rerank(
            query=query,
            documents=texts,
            top_n=len(docs),  # Return all documents, ranked
            model="command-r-plus-04-2024"  # Or a suitable model for your task
        )

        # Create a list of tuples (document, score)
        ranked_docs_with_scores = []
        for i, result in enumerate(response.results):
            ranked_docs_with_scores.append((docs[i], result.score))

        # Sort documents based on scores
        ranked_docs_with_scores.sort(key=lambda x: x[1], reverse=True)
        ranked_docs = [doc for doc, score in ranked_docs_with_scores]
        
        return ranked_docs