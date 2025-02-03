

from typing import Any
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_community.tools.tavily_search import TavilySearchResults

from graph.state import GraphState

load_dotenv()
web_search_tool = TavilySearchResults(max_results=5)

def web_search(state: GraphState) -> dict[str, Any]:
    print("--WEB SEARCH")
    question = state["question"]
    documents = state.get("documents", None)

    tavily_results = web_search_tool.invoke({"query": question})
    joined_tavily_results = "\n".join([result["content"] for result in tavily_results])

    web_results =  Document(page_content=joined_tavily_results)

    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]

    return {"documents": documents, "question": question}