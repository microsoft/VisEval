from __future__ import annotations

import json
import sys
import warnings

from langchain.chat_models.base import BaseChatModel
from langchain.schema import HumanMessage, SystemMessage

INSTRUCTION = """You will be provided with a visualization and its specifications. Consider the following aspect:

    - If the scale selected for the visualization is appropriate for accurate interpretation of values, avoid using unconventional scales, such as an inverted y-axis scale.
    - When axes are present, ensure that the selected ticks are appropriate for clarity, avoiding unconventional choices, such as representing counts of individual entities with floating-point ticks.


Report your findings, focusing solely on scale and tick appropriateness without considering the order.
```
    {
        "Appropriate": true/false,
        "Rationale": "reason ..."
    }
```
"""


def scale_and_ticks_check(context: dict, query: str, vision_model: BaseChatModel):
    base64 = context["base64"]
    encoding = context["encoding"]
    chart = context["chart"]
    if chart == "pie":
        ticks_desc = ""
    else:
        x_ticks = encoding["x"]["scale"]["ticks"]
        y_ticks = encoding["y"]["scale"]["ticks"]
        ticks_desc = f"Ticks extracted from the visualization:\n- x axis ticks: {','.join(x_ticks)}\n- y axis ticks: {','.join(y_ticks)}\n\n"
    try:
        messages = [
            SystemMessage(content=INSTRUCTION),
        ]
        messages.append(
            HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": f"Visualization specification:{query}\n\n{ticks_desc}Visualization image that has been verified for DATA and ORDER accuracy:",
                    },
                    {
                        "type": "image_url",
                        "image_url": base64,
                    },
                ]
            )
        )

        response = vision_model.invoke(messages)

        json_string = (
            response.content.replace("```json\n", "").replace("```", "").strip()
        )
        try:
            result = json.loads(json_string)
        except Exception:
            result = eval(json_string)
        return result["Appropriate"], result["Rationale"]
    except Exception:
        warnings.warn(str(sys.exc_info()))
    return None, "Exception occurred."
