"""
No framework baseline implementation of the agent.
"""
import json
import time
from typing import Dict, Any, List, Optional, Union

from common.schema import UserMessage, AgentResponse, AgentMetrics, ToolCall
from common.tools import execute_tool
from common.llm import LLMClient
from agents.base_agent import BaseAgent


class NoFrameworkAgent(BaseAgent):
    """
    Implementation of an agent using no framework, just raw LLM calls.
    """
    
    def __init__(self, model: str = None):
        """
        Initialize the agent.
        
        Args:
            model: The LLM model to use
        """
        self.llm = LLMClient(model=model)
        self.messages = []
        self.system_prompt = """
        You are a helpful assistant with access to the following tools:
        
        - get_weather: Get the current weather for a location
        - search_knowledge_base: Search a knowledge base for information
        - calculate: Evaluate a mathematical expression
        
        Use these tools when needed to provide accurate and helpful responses.
        """
        self.tool_definitions = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get the current weather for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The location to get weather for"
                            }
                        },
                        "required": ["location"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_knowledge_base",
                    "description": "Search a knowledge base for information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query"
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of results to return"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": "Evaluate a mathematical expression",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "The expression to evaluate"
                            }
                        },
                        "required": ["expression"]
                    }
                }
            }
        ]
        
        # Metrics
        self.total_tokens = 0
        self.start_time = time.time()
        self.tool_calls_count = 0
        self.error_count = 0
        
    def initialize(self) -> None:
        """
        Initialize the agent.
        """
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]
    
    def process(self, user_message: UserMessage) -> AgentResponse:
        """
        Process a user message and return a response.
        
        Args:
            user_message: The user message to process
            
        Returns:
            Agent's response
        """
        # Add user message to history
        self.messages.append({"role": "user", "content": user_message.content})
        
        # Process the conversation
        MAX_ITERATIONS = 10
        iteration = 0
        final_content = ""
        tool_calls = []
        
        while iteration < MAX_ITERATIONS:
            try:
                # Get LLM response
                response = self.llm.complete(
                    messages=self.messages,
                    tools=self.tool_definitions
                )
                
                # Update token count from response if available
                if hasattr(response, "usage") and response.usage:
                    self.total_tokens += response.usage.total_tokens
                
                # Extract assistant message
                assistant_message = response.choices[0].message
                
                # Add to conversation history
                self.messages.append(assistant_message)
                
                # Check if tool calls are required
                if hasattr(assistant_message, "tool_calls") and assistant_message.tool_calls:
                    self.tool_calls_count += len(assistant_message.tool_calls)
                    
                    # Process each tool call
                    for tool_call in assistant_message.tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        # Record the tool call
                        tool_calls.append(ToolCall(
                            tool_name=function_name,
                            tool_input=function_args
                        ))
                        
                        # Execute the tool
                        tool_result = execute_tool(function_name, function_args)
                        
                        # Add tool result to conversation
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(tool_result)
                        })
                    
                    # Continue to next iteration
                    iteration += 1
                    continue
                
                # If no tool calls, we're done
                final_content = assistant_message.content
                break
                
            except Exception as e:
                self.error_count += 1
                print(f"Error in agent processing: {e}")
                final_content = f"Error: {str(e)}"
                break
            
            iteration += 1
        
        # Return the final response
        return AgentResponse(
            content=final_content,
            tool_calls=tool_calls
        )
    
    def reset(self) -> None:
        """
        Reset the agent's state.
        """
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
    def get_metrics(self) -> AgentMetrics:
        """
        Get metrics about the agent's performance.
        
        Returns:
            AgentMetrics object with performance data
        """
        execution_time = time.time() - self.start_time
        
        return AgentMetrics(
            total_tokens=self.total_tokens,
            execution_time=execution_time,
            tool_calls_count=self.tool_calls_count,
            success_rate=1.0 if self.error_count == 0 else (1.0 - (self.error_count / self.tool_calls_count if self.tool_calls_count > 0 else 1.0)),
            error_count=self.error_count
        )
