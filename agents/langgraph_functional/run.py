"""
Run script for the LangGraph functional agent implementation.
"""
import sys
import os
import json
from typing import Dict, Any, List

# Add parent directory to path to allow imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_dir)

from common.schema import UserMessage
from agents.langgraph_functional.agent import LangGraphFunctionalAgent


def main():
    """
    Main function to run the agent.
    """
    # Create and initialize the agent
    agent = LangGraphFunctionalAgent()
    agent.initialize()
    
    print("\nLangGraph (Functional API) Agent")
    print("===============================")
    print("Type 'exit' to quit")
    print()
    
    while True:
        # Get user input
        user_input = input("User: ")
        
        if user_input.lower() in ["exit", "quit", "q"]:
            break
        
        # Process user input
        user_message = UserMessage(content=user_input)
        response = agent.process(user_message)
        
        # Display response
        print("\nAssistant:", response.content)
        
        # Display tool calls if any
        if response.tool_calls:
            print("\nTool Calls:")
            for i, tool_call in enumerate(response.tool_calls):
                print(f"  {i+1}. {tool_call.tool_name}({json.dumps(tool_call.tool_input, indent=2)})")
        
        print()
    
    # Display metrics at the end
    metrics = agent.get_metrics()
    print("\nAgent Metrics:")
    print(f"  Total tokens: {metrics.total_tokens}")
    print(f"  Execution time: {metrics.execution_time:.2f} seconds")
    print(f"  Tool calls count: {metrics.tool_calls_count}")
    print(f"  Success rate: {metrics.success_rate:.2%}")
    print(f"  Error count: {metrics.error_count}")


if __name__ == "__main__":
    main()
