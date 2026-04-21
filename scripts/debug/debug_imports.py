import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")

try:
    import langchain
    print(f"LangChain Version: {langchain.__version__}")
    print(f"LangChain Path: {langchain.__file__}")
    
    try:
        import langchain.chains
        print("✅ Successfully imported langchain.chains")
        print(f"Chains path: {langchain.chains.__file__}")
    except ImportError as e:
        print(f"❌ Failed to import langchain.chains: {e}")
        
    try:
        from langchain.chains import create_history_aware_retriever
        print("✅ Successfully imported create_history_aware_retriever")
    except ImportError as e:
        print(f"❌ Failed to import create_history_aware_retriever: {e}")

except ImportError as e:
    print(f"❌ Failed to import langchain: {e}")

print("\nInstalled Packages:")
# os.system("pip list")
