"""
Common schemas for agent inputs and outputs to ensure consistent comparison.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class UserMessage(BaseModel):
    """User message to the agent."""
    content: str = Field(..., description="The content of the message")
    

class ToolCall(BaseModel):
    """A tool call made by the agent."""
    tool_name: str = Field(..., description="The name of the tool to call")
    tool_input: Dict[str, Any] = Field(..., description="The input parameters for the tool")
    

class ToolResult(BaseModel):
    """The result of a tool call."""
    tool_name: str = Field(..., description="The name of the tool that was called")
    result: Any = Field(..., description="The result of the tool call")
    error: Optional[str] = Field(None, description="Error message if the tool call failed")


class AgentResponse(BaseModel):
    """The response from the agent to the user."""
    content: str = Field(..., description="The content of the agent's response")
    tool_calls: List[ToolCall] = Field(default_factory=list, description="Tool calls made by the agent")
    

class AgentConversation(BaseModel):
    """A conversation between a user and an agent."""
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="Messages in the conversation")
    

class AgentMetrics(BaseModel):
    """Metrics for evaluating agent performance."""
    total_tokens: int = Field(0, description="Total tokens used")
    execution_time: float = Field(0.0, description="Execution time in seconds")
    tool_calls_count: int = Field(0, description="Number of tool calls made")
    success_rate: float = Field(0.0, description="Success rate for completing tasks")
    error_count: int = Field(0, description="Number of errors encountered")
