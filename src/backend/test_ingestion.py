from backend.ingestion import load_documents

if __name__ == "__main__":
    with open("sample.pdf", "rb") as f:
        docs = load_documents([f])
        print(f"Extracted {len(docs)} chunks.")
        print("First metadata:", docs[0].metadata)
