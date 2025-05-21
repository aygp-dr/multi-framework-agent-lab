"""
Common tool implementations to be used across all agent frameworks.
"""
import json
import math
from typing import Dict, Any, List, Optional
import os
import datetime


def get_weather(location: str) -> Dict[str, Any]:
    """
    Get the current weather for a location.
    This is a mock implementation for demonstration purposes.
    
    Args:
        location: The location to get weather for
        
    Returns:
        Dict containing weather information
    """
    # Mock implementation
    return {
        "location": location,
        "temperature": 72,
        "conditions": "sunny",
        "humidity": 45,
        "wind_speed": 5,
        "timestamp": datetime.datetime.now().isoformat()
    }


def search_knowledge_base(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
    """
    Search a knowledge base for information.
    This is a mock implementation for demonstration purposes.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return
        
    Returns:
        List of search results
    """
    # Mock implementation
    results = [
        {"title": "Sample article 1", "content": f"This is a sample article about {query}", "relevance": 0.95},
        {"title": "Sample article 2", "content": f"Another article related to {query}", "relevance": 0.82},
        {"title": "Sample article 3", "content": f"Additional information about {query}", "relevance": 0.67},
        {"title": "Sample article 4", "content": f"Somewhat related to {query}", "relevance": 0.45},
    ]
    return results[:max_results]


def calculate(expression: str) -> Dict[str, Any]:
    """
    Evaluate a mathematical expression.
    
    Args:
        expression: The expression to evaluate
        
    Returns:
        Dict containing the result or error
    """
    try:
        # Safe evaluation using math module
        # This is a simplified version and not secure for production use
        allowed_names = {
            k: v for k, v in math.__dict__.items() 
            if not k.startswith('__')
        }
        
        # Add basic operations
        allowed_names.update({
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
        })
        
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return {
            "expression": expression,
            "result": result,
            "error": None
        }
    except Exception as e:
        return {
            "expression": expression,
            "result": None,
            "error": str(e)
        }


# Dictionary mapping tool names to their implementations
TOOLS = {
    "get_weather": get_weather,
    "search_knowledge_base": search_knowledge_base,
    "calculate": calculate,
}


def execute_tool(tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a tool by name with the provided input.
    
    Args:
        tool_name: The name of the tool to execute
        tool_input: The input parameters for the tool
        
    Returns:
        The result of the tool execution
    """
    if tool_name not in TOOLS:
        return {
            "error": f"Tool not found: {tool_name}",
            "result": None
        }
    
    try:
        tool_func = TOOLS[tool_name]
        result = tool_func(**tool_input)
        return {
            "error": None,
            "result": result
        }
    except Exception as e:
        return {
            "error": str(e),
            "result": None
        }
