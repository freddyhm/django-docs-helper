from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class GradeHallucination(BaseModel):
    """Binary score for hallucination present in generation answer."""

    binary_score: str = Field(
        description="Answer is grouned in the facts, 'yes' or 'no'",
    )

structured_llm_grader = llm.with_structured_output(GradeHallucination)

system =  """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n
     Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts."""

hallucination_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
])

hallucination_grader: RunnableSequence = hallucination_prompt | structured_llm_grader