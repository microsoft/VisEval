import time
from llmx import TextGenerator
from lida import Manager
from lida.datamodel import Goal
from lida.components import preprocess_code, get_globals_dict
import re
import ast
import importlib

import matplotlib.pyplot as plt
import pandas as pd

from .agent import Agent, ChartExecutionResult
from .utils import show_svg

max_retries = 20
retry_seconds = 20


class Lida(Agent):
    def __init__(self, llm: TextGenerator):
        self.lida = Manager(text_gen=llm)

    def generate(self, nl_query: str, tables: list[str], config: dict):
        library = config["library"]
        summary = self.lida.summarize(tables[0])

        for attempt in range(max_retries):
            try:
                charts = self.lida.visualize(
                    summary=summary, goal=nl_query, library=library, return_error=True
                )

                code = charts[0].code
                code += "\nplt.show()"

                context = {"data": self.lida.data, "library": library}
                return code, context
            except Exception:
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_seconds} seconds...")
                    time.sleep(retry_seconds)

        return None, None

    def execute(self, code: str, context: dict, log_name: str = None):
        data = context["data"]
        library = context["library"]

        code = preprocess_code(code)
        if library == "matplotlib" or library == "seaborn":
            try:
                ex_locals = get_globals_dict(code, data)
                exec(code, ex_locals)

                plt.box(False)
                plt.grid(color="lightgray", linestyle="dashed", zorder=-10)

                svg_string = show_svg(plt, log_name)
                return ChartExecutionResult(status=True, svg_string=svg_string)
            except Exception as exception_error:
                import traceback

                exception_info = traceback.format_exception_only(
                    type(exception_error), exception_error
                )
                return ChartExecutionResult(status=False, error_msg=exception_info)
        else:
            pass

    def evaluate(self, code: str, nl_query: str, library: str):
        goal = Goal(question=nl_query, visualization=nl_query, rationale="")

        result = self.lida.evaluate(code, goal, library=library)
        return result[0]
