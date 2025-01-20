from graph.constants import GRADE_DOCUMENTS, RETRIEVE
from graph.nodes import retrieve, grade_documents
from graph.state import GraphState
from langgraph.graph import END, StateGraph
from dotenv import load_dotenv

load_dotenv()

workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)

workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_edge(GRADE_DOCUMENTS, END)

workflow.set_entry_point(RETRIEVE)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")
