"""Tests for core agent functionality."""
import pytest
from multi_framework_agent.core import Agent


def test_agent_initialization():
    """Test that an agent can be initialized with name and config."""
    name = "test_agent"
    config = {"key": "value"}
    
    agent = Agent(name, config)
    
    assert agent.name == name
    assert agent.config == config


def test_agent_run_not_implemented():
    """Test that base Agent's run method raises NotImplementedError."""
    agent = Agent("test_agent")
    
    with pytest.raises(NotImplementedError):
        agent.run("test input")