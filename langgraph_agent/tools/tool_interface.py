# Placeholder for tools/tool_interface.py
# tools/tool_interface.py

from abc import ABC, abstractmethod

class ToolInterface(ABC):
    """
    Base interface for all security response tools.
    All tools should implement this interface to be compatible with the agent.
    """

    @abstractmethod
    def run(self, context: dict) -> dict:
        """
        Executes the tool with the given context.

        Args:
            context (dict): A dictionary containing input data, e.g., logs, traffic info.

        Returns:
            dict: Tool's output with actions, decisions, or logs.
        """
        pass
