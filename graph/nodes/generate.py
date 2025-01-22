from typing import Any
from graph.state import GraphState
from graph.chains.generation import generation_chain


def generate(state: GraphState) -> dict[str, Any]:
    print("Generating...")
    question = state["question"]
    documents = state["documents"]

    generation = generation_chain.invoke({"context": documents, "question": question})

    return {"question": question, "documents": documents, "generation": generation}