"""
Base agent interface that all implementations must follow.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from common.schema import UserMessage, AgentResponse, AgentMetrics


class BaseAgent(ABC):
    """
    Abstract base class for all agent implementations.
    """
    
    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the agent with any necessary setup.
        """
        pass
    
    @abstractmethod
    def process(self, user_message: UserMessage) -> AgentResponse:
        """
        Process a user message and return a response.
        
        Args:
            user_message: The user message to process
            
        Returns:
            Agent's response
        """
        pass
    
    @abstractmethod
    def reset(self) -> None:
        """
        Reset the agent's state.
        """
        pass
    
    @abstractmethod
    def get_metrics(self) -> AgentMetrics:
        """
        Get metrics about the agent's performance.
        
        Returns:
            AgentMetrics object with performance data
        """
        pass
