# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from __future__ import annotations

import json
import sys
import warnings

from langchain.chat_models.base import BaseChatModel
from langchain.schema import HumanMessage, SystemMessage

INSTRUCTION = """Your task is to evaluate the readability of the visualization on a scale of 1 to 5, where 1 indicates very difficult to read and 5 indicates very easy to read. You will be given a visualization requirement and the corresponding visualization created based on that requirement. Additionally, reviews from others regarding this visualization will be provided for your reference. Please think carefully and provide your reasoning and score.
```
    {
        "Rationale": "a brief reason",
        "Score": 1-5
    }
```


Examples:
- If the visualization is clear and information can be easily interpreted, you might return:
```
    {
        "Rationale": "The chart is well-organized, and the use of contrasting colors helps in distinguishing different data sets effectively. The labels are legible, and the key insights can be understood at a glance.",
        "Score": 5
    }
```
- Conversely, if the visualization is cluttered or confusing, you might return:
```
    {
        "Rationale": "While there is no overflow or overlap, the unconventional inverted y-axis and the use of decimal numbers for months on the x-axis deviate from the standard interpretation of bar charts, confusing readers and significantly affecting the chart's readability.",
        "Score": 1
    }
```
"""


def readability_check(context: dict, query: str, vision_model: BaseChatModel):
    base64 = context["base64"]

    reviews = ""
    if "reviews" in context and len(context["reviews"]) > 0:
        reviews = "Other Reviews:\n"
        reviews += "\n".join(
            [
                f"""- {review["aspect"]}: {review["content"]}"""
                for review in context["reviews"]
            ]
        )
        reviews += "\n\n"

    try:
        messages = [
            SystemMessage(content=INSTRUCTION),
        ]
        messages.append(
            HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": f"""Visualization Requirement: {query}\n\n{reviews}Visualization image:""",
                    },
                    {
                        "type": "image_url",
                        "image_url": base64,
                    },
                    {
                        "type": "text",
                        "text": """Please assess the readability, taking into account factors such as layout, scale and ticks, title and labels, colors, and ease of extracting information. Do not consider the correctness of the data and order in the visualizations, as they have already been verified.""",
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

        return result["Score"], result["Rationale"]
    except Exception:
        warnings.warn(str(sys.exc_info()))
    return None, "Exception occurred."
