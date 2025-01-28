from graph.chains.answer_grader import answer_grader
from graph.constants import GENERATE, GRADE_DOCUMENTS, RETRIEVE
from graph.nodes import generate, retrieve, grade_documents
from graph.state import GraphState
from graph.chains.hallucination_grader import hallucination_grader
from langgraph.graph import END, StateGraph
from dotenv import load_dotenv

load_dotenv()

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

workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)

workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_edge(GRADE_DOCUMENTS, GENERATE)
workflow.add_edge(GENERATE, END)

workflow.add_conditional_edges(GENERATE, grade_generation_grouned_in_documents_and_question,                               {
    "not supported": GENERATE,
    "not useful": GENERATE,
    "useful": END,
})


workflow.set_entry_point(RETRIEVE)

app = workflow.compile()

print("ok")

# app.get_graph().draw_mermaid_png(draw_mode="dark")
