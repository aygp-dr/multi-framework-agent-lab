"""Core functionality for multi-framework agent."""
from typing import Dict, List, Optional, Any


class Agent:
    """Base agent class for multi-framework implementations."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """Initialize agent with name and configuration.
        
        Args:
            name: The agent's name
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
        
    def run(self, input_data: Any) -> Dict[str, Any]:
        """Run the agent on input data.
        
        Args:
            input_data: The data to process
            
        Returns:
            Dictionary of results
        """
        raise NotImplementedError("Subclasses must implement run method")