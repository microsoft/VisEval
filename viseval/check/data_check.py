# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import copy
import json

from .time_utils import (
    compare_time_strings,
    convert_month_or_weekday_to_int,
    is_month_or_weekday,
    parse_number_to_time,
    parse_time_to_timestamp,
)

PRECISION = 0.0005


def is_numeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def compare_string(string, ground_truth):
    return string.strip().lower().startswith(ground_truth.strip().lower())

def convert_ground_truth_data(ground_truth):
    # ground truth data
    x_data = ground_truth["x_data"]
    y_data = ground_truth["y_data"]
    classify = ground_truth["classify"]

    data_ground_truth = []
    if len(classify) == 0:
        x_data = x_data[0]
        y_data = y_data[0]
        for index in range(len(x_data)):
            data_ground_truth.append(
                {
                    "field_x": x_data[index],
                    "field_y": y_data[index],
                }
            )
    else:
        # scatter
        if len(classify) == len(x_data) and len(classify) == len(y_data):
            for index in range(len(classify)):
                for index2 in range(len(x_data[index])):
                    data_ground_truth.append(
                        {
                            "field_x": x_data[index][index2],
                            "field_y": y_data[index][index2],
                            "field_classify": classify[index],
                        }
                    )
        # line / bar
        elif len(classify) == len(y_data):
            for index in range(len(classify)):
                for index2 in range(len(x_data[0])):
                    data_ground_truth.append(
                        {
                            "field_x": x_data[0][index2],
                            "field_y": y_data[index][index2],
                            "field_classify": classify[index],
                        }
                    )
    return data_ground_truth


# return answer and rationale for the data check
def compare_data(data_ground_truth, chart_info):
    # deep copy: avoid to change origin data
    data = copy.deepcopy(chart_info["data"])
    encoding = chart_info["encoding"]
    # line chart may have different length of data because line chart might omit some values
    if (len(data) != len(data_ground_truth) and chart_info["mark"] != "line") or (
        len(data) > len(data_ground_truth)
    ):
        return (
            False,
            f"visualization data length {len(data)} != ground truth length {len(data_ground_truth)}.",
        )

    if chart_info["mark"] == "arc":
        # field_fill -> field_x
        field_x = "field_fill"
        # field_theta -> field_y relative
        field_y = "field_theta"

        scale = None
        for datum_ground_truth in data_ground_truth:
            datum = [
                x
                for x in data
                if compare_string(str(x[field_x]), str(datum_ground_truth["field_x"]))
            ]
            if len(datum) == 1:
                datum = datum[0]
                if scale is None:
                    scale = datum[field_y] / datum_ground_truth["field_y"]
                else:
                    if (
                        abs(datum[field_y] / datum_ground_truth["field_y"] - scale)
                        > PRECISION
                    ):
                        return False, f"{json.dumps(datum_ground_truth)} not found\n"
            elif len(datum) == 0:
                return False, f"{json.dumps(datum_ground_truth)} not found."
            elif len(datum) > 1:
                return False, f"{json.dumps(datum_ground_truth)} found more than one."
    else:
        if len(encoding.keys()) < len(data_ground_truth[0].keys()):
            return False, "too few channels\n"
        elif len(encoding.keys()) > 3:
            return False, "too many channels\n"
        elif len(encoding.keys()) > len(data_ground_truth[0].keys()):
            # only keep x and y for comparison
            encoding = {key: encoding[key] for key in ["x", "y"]}

        for datum_ground_truth in data_ground_truth:
            datum = data
            for key in encoding:
                if key == "x" or key == "y":
                    field = f"field_{key}"
                else:
                    field = "field_classify"
                if (
                    encoding[key]["type"] == "quantitative"
                    or encoding[key]["type"] == "temporal"
                ):
                    # e.g., Monday -> 1
                    if is_month_or_weekday(datum_ground_truth[field]):
                        if encoding[key]["type"] == "temporal":
                            datum = [
                                x
                                for x in datum
                                if compare_time_strings(
                                    x["field_" + key].strip(),
                                    str(datum_ground_truth[field]).strip(),
                                )
                            ]
                            value_ground_truth = None
                        else:
                            value_ground_truth = convert_month_or_weekday_to_int(
                                datum_ground_truth[field]
                            )
                    else:
                        try:
                            value_ground_truth = float(datum_ground_truth[field])
                        except Exception:
                            # not a number
                            # try temporal
                            try:
                                value_ground_truth = parse_time_to_timestamp(
                                    datum_ground_truth[field]
                                )
                                if value_ground_truth is None:
                                    return (
                                        False,
                                        f"The data type of {key}({encoding[key]['type']}) is wrong.",
                                    )

                                if encoding[key]["type"] == "quantitative":
                                    for x in datum:
                                        x["field_" + key] = parse_number_to_time(
                                            x["field_" + key]
                                        )
                            except Exception:
                                return (
                                    False,
                                    f"The data type of {key}({encoding[key]['type']}) is wrong.",
                                )

                    field_vis = (
                        "field_" + key
                        if encoding[key]["type"] != "temporal"
                        else "field_" + key + "_origin"
                    )
                    if value_ground_truth is not None:
                        # avoid division by zero
                        datum = [
                            x
                            for x in datum
                            if abs((x[field_vis] - value_ground_truth)) <= PRECISION
                            or (
                                value_ground_truth != 0
                                and abs(
                                    (x[field_vis] - value_ground_truth)
                                    / value_ground_truth
                                )
                                <= PRECISION
                            )
                        ]
                elif encoding[key]["type"] == "nominal":
                    # exact match or time match
                    datum = [
                        x
                        for x in datum
                        if compare_string(x["field_" + key], str(datum_ground_truth[field]))
                        or compare_time_strings(
                            x["field_" + key].strip(),
                            str(datum_ground_truth[field]).strip(),
                        )
                    ]

            if len(datum) == 0:
                if (
                    chart_info["mark"] == "line"
                    and (
                        encoding["x"]["type"] == "quantitative"
                        or encoding["x"]["type"] == "temporal"
                    )
                    and (encoding["y"]["type"] == "quantitative")
                ):
                    # use all data
                    datum = chart_info["data"]
                    if len(data_ground_truth[0].keys()) == 3:
                        datum = [
                            x
                            for x in datum
                            if x["field_stroke"].strip()
                            == datum_ground_truth["field_classify"].strip()
                        ]
                    # line chart might omit some values
                    min_larger_index = -1
                    max_smaller_index = -1
                    # convert
                    field_vis = (
                        "field_x"
                        if encoding["x"]["type"] != "temporal"
                        else "field_x_origin"
                    )
                    value_ground_truth = datum_ground_truth["field_x"]
                    try:
                        value_ground_truth = float(value_ground_truth)
                    except Exception:
                        value_ground_truth = parse_time_to_timestamp(value_ground_truth)

                    for index in range(len(datum)):
                        if datum[index][field_vis] > value_ground_truth:
                            if (
                                min_larger_index == -1
                                or datum[index][field_vis]
                                < datum[min_larger_index][field_vis]
                            ):
                                min_larger_index = index
                        elif datum[index][field_vis] < value_ground_truth:
                            if (
                                max_smaller_index == -1
                                or datum[index][field_vis]
                                > datum[max_smaller_index][field_vis]
                            ):
                                max_smaller_index = index
                    if min_larger_index != -1 and max_smaller_index != -1:
                        if (
                            abs(
                                (
                                    datum[min_larger_index]["field_y"]
                                    - datum[max_smaller_index]["field_y"]
                                )
                            )
                            <= PRECISION
                            or abs(
                                (
                                    datum[min_larger_index]["field_y"]
                                    - datum_ground_truth["field_y"]
                                )
                            )
                            <= PRECISION
                        ):
                            continue
                        else:
                            return (
                                False,
                                f"{json.dumps(datum_ground_truth)} not found\n",
                            )
                return False, f"{json.dumps(datum_ground_truth)} not found."
            else:
                data.remove(datum[0])

    return True, "The data on the charts is consistent with the ground truth."


def data_check(chart_info: dict, data: dict, channel_specified: list):
    if ("data" not in chart_info) or (len(chart_info["data"]) == 0):
        return False, "The data on the charts cannot be understood."

    data_ground_truth = convert_ground_truth_data(data)
    # filter zero data
    if chart_info["mark"] == "bar":
        data_ground_truth = list(
            filter(lambda x: x["field_x"] != 0 and x["field_y"] != 0, data_ground_truth)
        )
        chart_info["data"] = list(
            filter(
                lambda x: x["field_x"] != 0 and x["field_y"] != 0,
                chart_info["data"],
            )
        )
    candidates = [data_ground_truth]
    # ground truth channel -> chart channel
    channel_maps = []
    if len(data["classify"]) == 0:
        # 2 channels
        channel_maps.append({"x": "x", "y": "y"})
        if "x" not in channel_specified and "y" not in channel_specified:
            # swap x and y
            data_ground_truth_copy = copy.deepcopy(data_ground_truth)
            for datum in data_ground_truth_copy:
                datum["field_x"], datum["field_y"] = (
                    datum["field_y"],
                    datum["field_x"],
                )
            candidates.append(data_ground_truth_copy)
            channel_maps.append({"x": "y", "y": "x"})
    else:
        # 3 channels
        channel_maps.append({"x": "x", "y": "y", "classify": "classify"})
        channels = ["x", "y", "classify"]
        if len(channel_specified) <= 1:
            swap_channels = list(set(channels) - set(channel_specified))
            data_ground_truth_copy = copy.deepcopy(data_ground_truth)
            for datum in data_ground_truth_copy:
                (
                    datum[f"field_{swap_channels[0]}"],
                    datum[f"field_{swap_channels[1]}"],
                ) = (
                    datum[f"field_{swap_channels[1]}"],
                    datum[f"field_{swap_channels[0]}"],
                )
            candidates.append(data_ground_truth_copy)
            channel_map = {"x": "x", "y": "y", "classify": "classify"}
            channel_map[swap_channels[0]], channel_map[swap_channels[1]] = (
                channel_map[swap_channels[1]],
                channel_map[swap_channels[0]],
            )
            channel_maps.append(channel_map)
        if len(channel_specified) == 0:
            # swap x and z
            data_ground_truth_copy = copy.deepcopy(candidates[0])
            for datum in data_ground_truth_copy:
                datum["field_x"], datum["field_classify"] = (
                    datum["field_classify"],
                    datum["field_x"],
                )
            candidates.append(data_ground_truth_copy)
            channel_maps.append({"x": "classify", "y": "y", "classify": "x"})
            # swap x and y, x and z
            data_ground_truth_copy = copy.deepcopy(candidates[1])
            for datum in data_ground_truth_copy:
                datum["field_y"], datum["field_classify"] = (
                    datum["field_classify"],
                    datum["field_y"],
                )
            candidates.append(data_ground_truth_copy)
            channel_maps.append({"x": "y", "y": "classify", "classify": "x"})
    cache = None
    for i in range(len(candidates)):
        candidate = candidates[i]
        channel_map = channel_maps[i]
        answer, rationale = compare_data(candidate, chart_info)
        if answer:
            chart_info["channel_map"] = channel_map
            return answer, rationale
        if i == 0:
            cache = [answer, rationale]

    return cache[0], cache[1]
