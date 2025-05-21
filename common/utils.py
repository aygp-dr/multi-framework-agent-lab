"""
Utility functions for the multi-framework agent lab.
"""
import json
import time
import os
from typing import Dict, Any, List, Optional, Callable
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def time_execution(func: Callable) -> Callable:
    """
    Decorator to measure execution time of a function.
    
    Args:
        func: The function to measure
        
    Returns:
        Wrapper function that times execution
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        print(f"Execution time for {func.__name__}: {execution_time:.4f} seconds")
        
        # Add execution time to result if it's a dict
        if isinstance(result, dict):
            result["execution_time"] = execution_time
            
        return result
    return wrapper


def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Load a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        The loaded JSON data
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return {}
        
        
def save_json_file(data: Dict[str, Any], file_path: str) -> bool:
    """
    Save data to a JSON file.
    
    Args:
        data: The data to save
        file_path: Path to save the JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving JSON file {file_path}: {e}")
        return False


def convert_to_openai_messages(conversation: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert internal message format to OpenAI message format.
    
    Args:
        conversation: List of messages in internal format
        
    Returns:
        List of messages in OpenAI format
    """
    openai_messages = []
    
    for msg in conversation:
        if msg.get("type") == "system":
            openai_messages.append({
                "role": "system",
                "content": msg.get("content", "")
            })
        elif msg.get("type") == "user":
            openai_messages.append({
                "role": "user",
                "content": msg.get("content", "")
            })
        elif msg.get("type") == "assistant":
            assistant_msg = {
                "role": "assistant",
                "content": msg.get("content", "")
            }
            
            # Add tool calls if present
            if "tool_calls" in msg and msg["tool_calls"]:
                assistant_msg["tool_calls"] = [
                    {
                        "id": f"call_{i}",
                        "type": "function",
                        "function": {
                            "name": tc["tool_name"],
                            "arguments": json.dumps(tc["tool_input"])
                        }
                    }
                    for i, tc in enumerate(msg["tool_calls"])
                ]
                
            openai_messages.append(assistant_msg)
        elif msg.get("type") == "tool":
            openai_messages.append({
                "role": "tool",
                "tool_call_id": msg.get("tool_call_id", "call_0"),
                "content": json.dumps(msg.get("content", {}))
            })
            
    return openai_messages
