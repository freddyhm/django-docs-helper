from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader

load_dotenv()

urls = [
    "https://docs.djangoproject.com/en/3.2/topics/db/queries/",
    # "https://docs.djangoproject.com/en/3.2/ref/models/querysets/"
    # "https://docs.djangoproject.com/en/3.2/topics/db/aggregation/"
    # "https://docs.djangoproject.com/en/3.2/topics/db/sql/"
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]
