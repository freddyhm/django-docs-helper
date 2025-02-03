from graph.chains.answer_grader import answer_grader
from graph.chains.router import question_router, RouteQuery
from graph.constants import ATTEMPTS_COUNTER, GENERATE, GRADE_DOCUMENTS, RETRIEVE, WEBSEARCH
from graph.nodes import generate, retrieve, grade_documents, web_search
from graph.state import GraphState
from graph.chains.hallucination_grader import hallucination_grader
from langgraph.graph import END, StateGraph
from dotenv import load_dotenv

load_dotenv()

def route_question(state: GraphState) -> str:
    print("--ROUTE QUESTION--")
    question = state["question"]
    source: RouteQuery = question_router.invoke({"question": question})
    if source.datasource == WEBSEARCH:
        print("---ROUTE QUESTION TO WEBSEARCH---")
        return WEBSEARCH
    elif source.datasource == RETRIEVE:
        print("---ROUTE QUESTION TO RAG---")
        return RETRIEVE
    return RETRIEVE

def decide_to_generate(state: GraphState) -> str:
    print("--ASSESS GRADED DOCUMENTS--")

    if state["web_search"]:
        print("--DECISION: NOT ALL DOCS ARE RELEVANT TO QUESTION, INCLUDE WEB SEARCH")
        return WEBSEARCH
    else:
        print("--DECISION: GENERATE")
        return RETRIEVE

def update_attempts_counter(state: GraphState) -> dict:
    """Node to increment attempts counter in state"""
    print("--INCREMENT ATTEMPTS COUNTER--")
    return {"attempts": state.get("attempts", 0) + 1}

def grade_generation_grouned_in_documents_and_question(state: GraphState) -> str:
    print("--CHECK HALLUCINATIONS--")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    hallucination_score = hallucination_grader.invoke({"documents": documents, "generation": generation})

    if hallucination_score.binary_score == "yes":
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        print("---GRADE GENERATION vs QUESTION---")
        answer_score = answer_grader.invoke({"question": question, "generation": generation})
        if answer_score.binary_score:
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"

def check_attempts(state: GraphState) -> str:
    """Check if max attempts reached"""
    print("--CHECK ATTEMPTS--")
    attempts = state.get("attempts", 0)
    if attempts >= 3:
        print("---MAX ATTEMPTS REACHED (3)---")
        return "max_attempts"
    return "continue"

workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)
workflow.add_node(ATTEMPTS_COUNTER, update_attempts_counter)

workflow.set_conditional_entry_point(
    route_question,
    {
        WEBSEARCH: WEBSEARCH,
        RETRIEVE: RETRIEVE,
    }
)

workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_edge(GRADE_DOCUMENTS, GENERATE)
workflow.add_edge(WEBSEARCH, GENERATE)

workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    {
        WEBSEARCH: WEBSEARCH,
        RETRIEVE: RETRIEVE,
    },
)

workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grouned_in_documents_and_question,
    {
        "not supported": ATTEMPTS_COUNTER,
        "not useful": ATTEMPTS_COUNTER,
        "useful": END,
    }
)

workflow.add_conditional_edges(
    ATTEMPTS_COUNTER,
    check_attempts,
    {
        "continue": GENERATE,
        "max_attempts": END,
    }
)

workflow.add_edge(GENERATE, END)

app = workflow.compile()

# app.get_graph().draw_mermaid_png(draw_mode="dark")
