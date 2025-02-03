from typing import Dict, Any
from graph.state import GraphState
from ingestion import retriever


def retrieve(state: GraphState) -> Dict[str, Any]:
    print("\nRetrieving documents...")
    question = state["question"]  # coming from the user

    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}