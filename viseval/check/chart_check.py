# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.


def chart_check(
    chart_info: dict, chart_type_ground_truth: str, stacked_bar: bool = False
):
    # chart_type_ground_truth: pie, bar, line, scatter, stacked bar, grouping line, grouping scatter
    if "chart" not in chart_info:
        return False, "Cannot recognize the chart type."

    chart_type = chart_info["chart"]

    if chart_type_ground_truth.lower() in chart_type.lower() or (
        chart_type_ground_truth == "Stacked Bar"
        and not stacked_bar
        and "grouping bar" in chart_type.lower()
    ):
        return True, "Chart type is consistent with ground truth."

    return False, "Chart type is not consistent with ground truth."
