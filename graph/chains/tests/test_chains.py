from dotenv import load_dotenv
from graph.chains.retrieval_grader import GradeDocuments, retrieval_grader
from ingestion import retriever
from graph.chains.hallucination_grader import GradeHallucination, hallucination_grader
from graph.chains.generation import generation_chain



load_dotenv()


def test_retrival_grader_answer_yes() -> None:
    question = "How to make queries?"
    docs = retriever.invoke(question)
    doc_txt = docs[1].page_content

    # grade relevant question related to relevant doc
    res: GradeDocuments = retrieval_grader.invoke(
        {"question": "How to save changes to objects?", "document": doc_txt}
    )

    assert res.binary_score == "yes"


def test_retrival_grader_answer_no() -> None:
    # retrieve relevant docs
    question = "How to make queries?"
    docs = retriever.invoke(question)
    doc_txt = docs[1].page_content

    # grade irrelevant question related to relevant doc
    res: GradeDocuments = retrieval_grader.invoke(
        {"question": "What is agent memory?", "document": doc_txt}
    )

    assert res.binary_score == "no"

def test_generation_chain() -> None:
    question = "How to make queries?"
    docs = retriever.invoke(question)
    generation = generation_chain.invoke({"context": docs, "question": question})
    print(generation)


def test_hallucination_grader_answer_yes() -> None:
    question = "How to make queries?"
    docs = retriever.invoke(question)
    generation = generation_chain.invoke({"context": docs, "question": question})

    res: GradeHallucination = hallucination_grader.invoke(
        {"documents": docs, "generation": generation}
    )

    assert res.binary_score == "yes"


def test_hallucination_grader_answer_no() -> None:
    question = "How to make queries?"
    docs = retriever.invoke(question)

    res: GradeHallucination = hallucination_grader.invoke(
        {
            "documents": docs,
            "generation": "In order to make pizza we need to first start with the dough",
        }
    )

    assert res.binary_score == "no"

# def test_router_to_vectorstore() -> None:
#     question = "agent memory"

#     res: RouteQuery = question_router.invoke({"question": question})
#     assert res.datasource == "vectorstore"


# def test_router_to_websearch() -> None:
#     question = "how to make pizza"

#     res: RouteQuery = question_router.invoke({"question": question})
#     assert res.datasource == "websearch"