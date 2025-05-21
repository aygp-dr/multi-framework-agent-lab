"""
LangGraph (functional API) implementation of the agent.
"""
import json
import time
from typing import Dict, Any, List, Optional, Union, TypedDict, Annotated

from common.schema import UserMessage, AgentResponse, AgentMetrics, ToolCall
from common.tools import execute_tool
from common.llm import LLMClient
from agents.base_agent import BaseAgent

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent


# Define state for the graph
class AgentState(TypedDict):
    messages: List[Dict[str, Any]]
    tool_calls: List[Dict[str, Any]]
    current_tool_call: Optional[Dict[str, Any]]
    current_tool_result: Optional[Dict[str, Any]]
    response: Optional[str]


class LangGraphFunctionalAgent(BaseAgent):
    """
    Implementation of an agent using LangGraph's functional API.
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
        
        # Set up the LangGraph agent
        self._setup_graph()
        
        # Metrics
        self.total_tokens = 0
        self.start_time = time.time()
        self.tool_calls_count = 0
        self.error_count = 0
        
    def _setup_graph(self):
        """
        Set up the LangGraph agent.
        """
        # Define available tools
        tools = {
            "get_weather": lambda params: execute_tool("get_weather", params),
            "search_knowledge_base": lambda params: execute_tool("search_knowledge_base", params),
            "calculate": lambda params: execute_tool("calculate", params)
        }
        
        # Create the agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=tools,
            system_prompt=self.system_prompt
        )
        
        # Define the state graph
        builder = StateGraph(AgentState)
        
        # Add the agent node
        builder.add_node("agent", self.agent)
        
        # Define edges
        builder.add_edge("agent", END)
        
        # Compile the graph
        self.graph = builder.compile()
        
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
        
        # Run the graph
        try:
            # Initialize graph state
            state = AgentState(
                messages=self.messages.copy(),
                tool_calls=[],
                current_tool_call=None,
                current_tool_result=None,
                response=None
            )
            
            # Execute the graph
            result = self.graph.invoke(state)
            
            # Extract final messages
            final_messages = result["messages"]
            self.messages = final_messages
            
            # Extract tool calls
            tool_calls_list = []
            for msg in final_messages:
                if msg.get("role") == "assistant" and "tool_calls" in msg:
                    for tc in msg["tool_calls"]:
                        self.tool_calls_count += 1
                        tool_calls_list.append(ToolCall(
                            tool_name=tc["function"]["name"],
                            tool_input=json.loads(tc["function"]["arguments"])
                        ))
            
            # Find the final assistant message
            final_content = ""
            for msg in reversed(final_messages):
                if msg.get("role") == "assistant" and msg.get("content"):
                    final_content = msg["content"]
                    break
            
            return AgentResponse(
                content=final_content,
                tool_calls=tool_calls_list
            )
            
        except Exception as e:
            self.error_count += 1
            print(f"Error in LangGraph agent processing: {e}")
            return AgentResponse(
                content=f"Error: {str(e)}",
                tool_calls=[]
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
