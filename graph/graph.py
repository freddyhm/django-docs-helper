from graph.constants import RETRIEVE
from graph.nodes.retrieve import retrieve
from graph.state import GraphState
from langgraph.graph import END, StateGraph
from dotenv import load_dotenv

load_dotenv()

workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE, retrieve)

workflow.add_edge(RETRIEVE, END)

workflow.set_entry_point(RETRIEVE)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")
