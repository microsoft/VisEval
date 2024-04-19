from __future__ import annotations

import pandas as pd
import sys
import warnings
from langchain.chat_models.base import BaseChatModel
from langchain.schema import HumanMessage

from .utils import show_svg
from .agent import Agent, ChartExecutionResult

MAXIMUM_SAMPLES = 10

TEMPLATE = '''"""Use a dataframe called df from data_file.csv with columns {columns}.

{columns_description}

Label the x and y axes appropriately. Add a title. Set the fig suptitle as empty.

Using Python version 3.9.12 and library {library}, create a script using the dataframe df to graph the following: {nl_query}.
"""

{pre_code}
'''


class Chat2vis(Agent):
    def __init__(self, llm: BaseChatModel):
        self.llm = llm

    def table_format(self, data: pd.DataFrame):
        # table format
        descriptions = []
        for column in data.columns:
            dtype = data[column].dtype
            description = None
            if dtype in [int, float, complex]:
                description = f"The column '{column}' is type {dtype} and contains numeric values."
            elif dtype == bool:
                description = f"The column '{column}' is type {dtype} and contains boolean values."
            elif dtype == object:
                # Check if the string column can be cast to a valid datetime
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        pd.to_datetime(data[column], errors="raise")
                        dtype = "date"
                except ValueError:
                    # Check if the string column has a limited number of values
                    if data[column].nunique() / len(data[column]) < 0.5:
                        dtype = "category"
                    else:
                        dtype = "string"
            elif pd.api.types.is_categorical_dtype(data[column]):
                dtype = "category"
            elif pd.api.types.is_datetime64_any_dtype(data[column]):
                dtype = "date"

            if dtype == "date" or dtype == "category":
                non_null_values = data[column][data[column].notnull()].unique()
                n_samples = min(MAXIMUM_SAMPLES, len(non_null_values))
                samples = (
                    pd.Series(non_null_values)
                    .sample(n_samples, random_state=42)
                    .tolist()
                )
                values = "'" + "', '".join(samples) + "'"
                description = f"The column '{column}' has {dtype} values {values}"

                if n_samples < len(non_null_values):
                    description += " etc."
                else:
                    description += "."
            elif description is None:
                description = f"The column '{column}' is {dtype} type."

            descriptions.append(description)

        return " ".join(descriptions)

    def generate(self, nl_query: str, tables: list[str], config: dict):
        library = config["library"]

        if library == "seaborn":
            import_statements = "import seaborn as sns\n"
        else:
            import_statements = ""

        pre_code = f"""import pandas as pd
import matplotlib.pyplot as plt
{import_statements}
fig,ax = plt.subplots(1,1,figsize=(10,4))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

df=df_nvBenchEval.copy()
"""
        data = pd.read_csv(tables[0], encoding="utf-8")
        columns = "'" + "', '".join(list(data.columns)) + "'"
        prompt = TEMPLATE.format(
            columns=columns,
            columns_description=self.table_format(data),
            library=library,
            nl_query=nl_query,
            pre_code=pre_code,
        )

        try:
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            code = response.content
            codes = code.split("\n")
            codes = list(filter(lambda row: "data_file.csv" not in row, codes))
            code = "\n".join(codes)
            # plot.show
            if "plt.show()" not in code and ("plt." in code or "fig." in code):
                code += "\nplt.show()"

            context = {
                "tables": tables,
            }
            return pre_code + "\n" + code, context
        except Exception:
            warnings.warn(str(sys.exc_info()))
        return None, None

    def execute(self, code: str, context: dict, log_name: str = None):
        tables = context["tables"]
        df_nvBenchEval = pd.read_csv(tables[0])
        global_env = {
            "df_nvBenchEval": df_nvBenchEval,
            "svg_string": None,
            "show_svg": show_svg,
            "svg_name": log_name,
        }
        code += "\nsvg_string = show_svg(plt, svg_name)"
        try:
            exec(code, global_env)
            svg_string = global_env["svg_string"]
            return ChartExecutionResult(status=True, svg_string=svg_string)
        except Exception as exception_error:
            import traceback

            exception_info = traceback.format_exception_only(
                type(exception_error), exception_error
            )
            return ChartExecutionResult(status=False, error_msg=exception_info)
