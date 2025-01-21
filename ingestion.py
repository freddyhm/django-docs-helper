from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

load_dotenv()

urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0)
docs_split = text_splitter.split_documents(docs_list)

collection_name = "agent-docs"
persist_directory = "./.chroma"
embeddings = OpenAIEmbeddings()

chroma_db = Chroma(
    collection_name=collection_name,
    persist_directory=persist_directory,
    embedding_function=embeddings,
)

# if len(chroma_db.get()['documents']) == 0:
# vectorstore = Chroma.from_documents(
#     documents=docs_split,
#     collection_name=collection_name,
#     embedding=embeddings,
#     persist_directory=persist_directory,
# )

retriever = Chroma(
    collection_name=collection_name,
    persist_directory=persist_directory,
    embedding_function=embeddings,
).as_retriever()
