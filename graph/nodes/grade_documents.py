from typing import Any
from graph.state import GraphState
from graph.chains.retrieval_grader import retrieval_grader


def grade_documents(state: GraphState) -> dict[str, Any]:

    print("Grading documents...")
    question = state["question"]
    documents = state["documents"]

    filtered_docs = []

    for doc in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": doc}
        )
        grade = score.binary_score
        if grade.lower() == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(doc)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")

    return {"documents": filtered_docs, "question": question}

