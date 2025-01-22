from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# expects context and question as input variables
prompt = hub.pull("rlm/rag-prompt")

generation_chain = prompt | llm | StrOutputParser()
