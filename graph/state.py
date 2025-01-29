

from typing import TypedDict


class GraphState(TypedDict):
    question: str
    documents: list[str]
    generation: str
    attempts: int