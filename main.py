from dotenv import load_dotenv
from graph.graph import app

load_dotenv()

if __name__ == "__main__":
    result = app.invoke(input={"question": "How to make pizza?"})

    print("\n=== Question ===")
    print(result["question"])

    print("\n=== Documents Used ===")
    for i, doc in enumerate(result["documents"], 1):
        print(f"\nDocument {i}:")
        print(f"Source: {doc.metadata['source']}")
        print(f"Title: {doc.metadata['title']}")
        print(f"Content: {doc.page_content}")

    print("\n=== Generated Answer ===")
    print(result["generation"])
