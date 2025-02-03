from dotenv import load_dotenv
from graph.graph import app

load_dotenv()

if __name__ == "__main__":
    result = app.invoke(input={"question": "How to make queries?"})

    print("\n=== Question ===")
    print(result["question"])

    print("\n=== Documents Used ===")
    documents: list[str] = result["documents"]
    for i, doc in enumerate(documents, 1):
        print(f"\nDocument {i}:")
        print(f"Source: {doc.metadata['source'] if doc.metadata else 'N/A'}")
        print(f"Title: {doc.metadata['title'] if doc.metadata else 'N/A'}")
        print(f"Content: {doc.page_content}")

    print("\n=== Generated Answer ===")
    print(result["generation"])
