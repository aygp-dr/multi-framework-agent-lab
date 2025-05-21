"""
Verify that all expected directories and files have been created.
"""
import os
import sys

def print_status(message, success):
    """Print a status message with color."""
    if success:
        print(f"\033[92m✓ {message}\033[0m")
    else:
        print(f"\033[91m✗ {message}\033[0m")

def verify_structure():
    """
    Verify that the expected directory structure exists.
    """
    expected_dirs = [
        "agents",
        "agents/no_framework",
        "agents/langgraph_functional",
        "agents/langgraph_high_level",
        "agents/dspy",
        "agents/google_adk",
        "agents/inspect_ai",
        "agents/pydantic_ai",
        "agents/smolagents",
        "agents/agno",
        "common",
        "tests",
        "docs",
        "notebooks",
        "evaluation"
    ]
    
    expected_files = [
        "README.md",
        "requirements.txt",
        "Makefile",
        ".gitignore",
        "common/schema.py",
        "common/tools.py",
        "common/utils.py",
        "common/llm.py",
        "agents/base_agent.py",
        "agents/no_framework/agent.py",
        "agents/no_framework/run.py",
        "agents/langgraph_functional/agent.py",
        "agents/langgraph_functional/run.py",
        "evaluation/compare_all.py"
    ]
    
    success = True
    
    # Check directories
    print("Checking directories...")
    for dir_path in expected_dirs:
        if os.path.isdir(dir_path):
            print_status(f"Directory exists: {dir_path}", True)
        else:
            print_status(f"Directory missing: {dir_path}", False)
            success = False
    
    # Check files
    print("\nChecking files...")
    for file_path in expected_files:
        if os.path.isfile(file_path):
            print_status(f"File exists: {file_path}", True)
        else:
            print_status(f"File missing: {file_path}", False)
            success = False
    
    return success

if __name__ == "__main__":
    print("Multi-Framework Agent Lab Structure Verification")
    print("==============================================")
    
    success = verify_structure()
    
    if success:
        print("\n\033[92mAll expected directories and files exist!\033[0m")
        sys.exit(0)
    else:
        print("\n\033[91mSome expected directories or files are missing.\033[0m")
        sys.exit(1)
