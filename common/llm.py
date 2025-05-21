"""
Common LLM client wrapper to ensure consistent access across frameworks.
"""
import os
import json
from typing import Dict, Any, List, Optional, Union
from dotenv import load_dotenv
import litellm

# Load environment variables
load_dotenv()

# Initialize LiteLLM
litellm.api_key = os.getenv("OPENAI_API_KEY", "")
litellm.set_verbose = True if os.getenv("DEBUG", "False").lower() == "true" else False

# Default model to use (can be overridden)
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4-turbo")


class LLMClient:
    """
    Wrapper around LiteLLM for consistent LLM access.
    """
    
    def __init__(self, model: str = None, temperature: float = 0.7):
        """
        Initialize the LLM client.
        
        Args:
            model: The LLM model to use
            temperature: Temperature for LLM sampling
        """
        self.model = model or DEFAULT_MODEL
        self.temperature = temperature
        
    def complete(self, 
                messages: List[Dict[str, Any]], 
                tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Complete a conversation with the LLM.
        
        Args:
            messages: List of messages in the conversation
            tools: List of tools available to the LLM
            
        Returns:
            LLM response
        """
        try:
            response = litellm.completion(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                tools=tools,
                tool_choice="auto" if tools else None
            )
            return response
        except Exception as e:
            print(f"Error calling LLM: {e}")
            # Return a minimal error response
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": f"Error: Unable to get a response from the LLM. {str(e)}"
                        }
                    }
                ],
                "error": str(e)
            }

    def stream_complete(self, 
                       messages: List[Dict[str, Any]], 
                       tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Stream a completion from the LLM.
        
        Args:
            messages: List of messages in the conversation
            tools: List of tools available to the LLM
            
        Returns:
            Generator yielding LLM response chunks
        """
        try:
            response = litellm.completion(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                tools=tools,
                tool_choice="auto" if tools else None,
                stream=True
            )
            return response
        except Exception as e:
            print(f"Error streaming from LLM: {e}")
            # Return a minimal error response that mimics the stream format
            def error_generator():
                yield {
                    "choices": [
                        {
                            "delta": {
                                "role": "assistant",
                                "content": f"Error: Unable to get a response from the LLM. {str(e)}"
                            }
                        }
                    ],
                    "error": str(e)
                }
            return error_generator()
