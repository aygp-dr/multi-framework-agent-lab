"""
Script to compare all agent implementations.
"""
import sys
import os
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Any, List

# Add parent directory to path to allow imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from common.schema import UserMessage, AgentMetrics
# Import all agent implementations
from agents.no_framework.agent import NoFrameworkAgent
from agents.langgraph_functional.agent import LangGraphFunctionalAgent

# List of test queries to run against all agents
TEST_QUERIES = [
    "What's the weather like in Boston?",
    "Can you calculate 345 * 892?",
    "Search for information about artificial intelligence",
    "What's 25% of 840?",
    "Can you tell me about the capital of France and what the weather is like there right now?"
]


def run_comparison():
    """
    Run the comparison between all agent implementations.
    """
    # List of agent classes to test
    agent_classes = [
        ("No Framework", NoFrameworkAgent),
        ("LangGraph (Functional)", LangGraphFunctionalAgent),
        # Add other agent implementations as they are created
    ]
    
    results = []
    
    for agent_name, agent_class in agent_classes:
        print(f"\nTesting {agent_name} Agent")
        print("="*40)
        
        # Create and initialize the agent
        agent = agent_class()
        agent.initialize()
        
        # Track metrics for this agent
        agent_metrics = {
            "name": agent_name,
            "execution_times": [],
            "token_counts": [],
            "tool_calls": [],
            "errors": [],
            "responses": []
        }
        
        # Run each test query
        for i, query in enumerate(TEST_QUERIES):
            print(f"\nQuery {i+1}: {query}")
            
            # Process the query
            start_time = time.time()
            user_message = UserMessage(content=query)
            response = agent.process(user_message)
            
            # Record time
            query_time = time.time() - start_time
            agent_metrics["execution_times"].append(query_time)
            
            # Display and record response
            print(f"Response: {response.content[:100]}...")
            agent_metrics["responses"].append({
                "query": query,
                "response": response.content,
                "tool_calls": [tc.dict() for tc in response.tool_calls]
            })
            
            # Get updated metrics
            metrics = agent.get_metrics()
            
            # Record metrics
            agent_metrics["token_counts"].append(metrics.total_tokens)
            agent_metrics["tool_calls"].append(metrics.tool_calls_count)
            agent_metrics["errors"].append(metrics.error_count)
            
            # Reset agent for next query
            agent.reset()
        
        # Calculate aggregate metrics
        avg_execution_time = sum(agent_metrics["execution_times"]) / len(agent_metrics["execution_times"])
        total_tokens = agent_metrics["token_counts"][-1]  # Last recorded value
        total_tool_calls = agent_metrics["tool_calls"][-1]  # Last recorded value
        total_errors = agent_metrics["errors"][-1]  # Last recorded value
        
        # Add to results
        results.append({
            "name": agent_name,
            "avg_execution_time": avg_execution_time,
            "total_tokens": total_tokens,
            "total_tool_calls": total_tool_calls,
            "total_errors": total_errors,
            "detailed_metrics": agent_metrics
        })
        
        print(f"\n{agent_name} Agent Summary:")
        print(f"  Average execution time: {avg_execution_time:.2f} seconds")
        print(f"  Total tokens: {total_tokens}")
        print(f"  Total tool calls: {total_tool_calls}")
        print(f"  Total errors: {total_errors}")
    
    # Save detailed results
    os.makedirs("evaluation/results", exist_ok=True)
    with open("evaluation/results/comparison_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Create comparison charts
    create_comparison_charts(results)
    
    return results


def create_comparison_charts(results: List[Dict[str, Any]]):
    """
    Create comparison charts from the results.
    
    Args:
        results: List of agent results
    """
    # Extract data for charts
    names = [r["name"] for r in results]
    exec_times = [r["avg_execution_time"] for r in results]
    tokens = [r["total_tokens"] for r in results]
    tool_calls = [r["total_tool_calls"] for r in results]
    errors = [r["total_errors"] for r in results]
    
    # Create figure with multiple subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle("Agent Framework Comparison", fontsize=16)
    
    # Execution time chart
    axes[0, 0].bar(names, exec_times)
    axes[0, 0].set_title("Average Execution Time (s)")
    axes[0, 0].set_ylabel("Seconds")
    axes[0, 0].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Token usage chart
    axes[0, 1].bar(names, tokens)
    axes[0, 1].set_title("Total Tokens Used")
    axes[0, 1].set_ylabel("Count")
    axes[0, 1].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Tool calls chart
    axes[1, 0].bar(names, tool_calls)
    axes[1, 0].set_title("Total Tool Calls")
    axes[1, 0].set_ylabel("Count")
    axes[1, 0].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Errors chart
    axes[1, 1].bar(names, errors)
    axes[1, 1].set_title("Total Errors")
    axes[1, 1].set_ylabel("Count")
    axes[1, 1].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Save the figure
    os.makedirs("evaluation/results", exist_ok=True)
    plt.savefig("evaluation/results/comparison_charts.png")
    

def main():
    """
    Main function.
    """
    print("Running Agent Framework Comparison")
    print("=================================")
    
    results = run_comparison()
    
    print("\nComparison complete! Results saved to evaluation/results/")


if __name__ == "__main__":
    main()
