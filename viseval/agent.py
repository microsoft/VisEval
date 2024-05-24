from abc import ABC, abstractmethod
from typing import Optional, Tuple, Union

from attr import dataclass
from langchain.chat_models.base import BaseChatModel
from llmx import TextGenerator


@dataclass
class ChartExecutionResult:
    """Response from a visualization execution"""

    # True if successful, False otherwise
    status: bool
    # Generate svg string if status is True
    svg_string: Optional[str] = None
    # Error message if status is False
    error_msg: Optional[str] = None


class Agent(ABC):
    @abstractmethod
    def __init__(
        self, llm: Union[BaseChatModel, TextGenerator], config: dict = None
    ) -> None:
        pass

    @abstractmethod
    def generate(
        self, nl_query: str, tables: list[str], config: dict
    ) -> Tuple[str, dict]:
        """Generate code for the given natural language query.

        Args:
            nl_query (str): Natural language query.
            tables (list[str]): List of table file paths.
            config (dict): Generation configuration.

        Returns:
            Tuple[str, dict]: Generated code and execution context.
        """
        pass

    @abstractmethod
    def execute(
        self, code: str, context: dict, log_name: str = None
    ) -> ChartExecutionResult:
        """Execute the given code with context and return the result

        Args:
            code (str): Code to execute,.
            context (dict): Context for the code execution. Different agents require different contexts.
            log_name (str, optional): SVG file name. Defaults to None.

        Returns:
            ChartExecutionResult: _description_
        """
        pass
