from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

load_dotenv()

urls = [
    "https://docs.djangoproject.com/en/3.2/topics/db/queries/",
    # "https://docs.djangoproject.com/en/3.2/ref/models/querysets/"
    # "https://docs.djangoproject.com/en/3.2/topics/db/aggregation/"
    # "https://docs.djangoproject.com/en/3.2/topics/db/sql/"
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0)

docs_split = text_splitter.split_documents(docs_list)

retriever = Chroma(
    collection_name="django-docs",
    persist_directory="./.chroma",
    embedding_function=OpenAIEmbeddings(),
).as_retriever()
