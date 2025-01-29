from graph.chains.answer_grader import answer_grader
from graph.constants import ATTEMPTS_COUNTER, GENERATE, GRADE_DOCUMENTS, RETRIEVE
from graph.nodes import generate, retrieve, grade_documents
from graph.state import GraphState
from graph.chains.hallucination_grader import hallucination_grader
from langgraph.graph import END, StateGraph
from dotenv import load_dotenv

load_dotenv()

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
workflow.add_node(ATTEMPTS_COUNTER, update_attempts_counter)

workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_edge(GRADE_DOCUMENTS, GENERATE)

workflow.add_conditional_edges(
    ATTEMPTS_COUNTER,
    check_attempts,
    {
        "continue": GENERATE,
        "max_attempts": END,
    }

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

workflow.set_entry_point(RETRIEVE)

app = workflow.compile()

# app.get_graph().draw_mermaid_png(draw_mode="dark")
