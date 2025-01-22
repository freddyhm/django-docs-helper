from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0)
docs_split = text_splitter.split_documents(documents=docs_list)

# collection_name = "agent-docs"
# persist_directory = "./.chroma"
embeddings = OpenAIEmbeddings()

vectorstore = FAISS.from_documents(docs_split, embeddings)
vectorstore.save_local("./faiss_index_react")

new_vectorstore = FAISS.load_local("./faiss_index_react", embeddings, allow_dangerous_deserialization=True)

retriever = new_vectorstore.as_retriever()
