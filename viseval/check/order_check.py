# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.


def order_check(chart_info: dict, ground_truth: dict, sort_by: str):
    order = ground_truth["sort"]
    encoding = chart_info["encoding"]
    data = chart_info["data"]
    channel_map = chart_info["channel_map"]

    if order is not None:
        # bar, line
        if sort_by == "axis":
            order_channel = order["channel"]
        else:
            order_channel = channel_map[order["channel"]]

        other_channel = "y" if order_channel == "x" else "x"

        order_channel_scale = encoding[order_channel]["scale"]
        other_channel_scale = encoding[other_channel]["scale"]

        # origin channel
        if (
            channel_map[order_channel] == "x"
            or channel_map[order_channel] == "classify"
        ):
            arr = []
            if len(order_channel_scale["range"]) == 0:
                scale_range = range(1, 1 + len(order_channel_scale["domain"]))
            else:
                scale_range = order_channel_scale["range"]

            for index in range(len(order_channel_scale["domain"])):
                arr.append(
                    tuple(
                        [
                            order_channel_scale["domain"][index],
                            scale_range[index],
                        ]
                    )
                )
            if order_channel == "x":
                reverse = True
            else:
                reverse = False
            if order["order"] == "ascending":
                arr.sort(key=lambda x: x[0], reverse=reverse)
            elif order["order"] == "descending":
                arr.sort(key=lambda x: x[0], reverse=not reverse)
            else:  # custom order
                sort_order = {}
                for index in range(len(order["order"])):
                    sort_order[order["order"][index]] = index
                arr.sort(key=lambda x: sort_order[x[0]], reverse=reverse)

            is_sorted = all([arr[i][1] > arr[i + 1][1] for i in range(len(arr) - 1)])
        # 'quantitative'
        else:
            # sort by other channel
            values_other = []
            for index in range(len(other_channel_scale["domain"])):
                values_other.append(
                    tuple(
                        [
                            other_channel_scale["domain"][index],
                            other_channel_scale["range"][index],
                        ]
                    )
                )
            values_other.sort(key=lambda x: x[1])
            values_other = [item[0] for item in values_other]

            # cumulative
            values_order = []
            for value in values_other:
                data_filter = [
                    float(d["field_" + order_channel])
                    for d in data
                    if d["field_" + other_channel] == value
                ]
                values_order.append(sum(data_filter))

            # filter zero data
            if chart_info["mark"] == "bar":
                values_order = list(filter(lambda x: x != 0, values_order))

            is_sorted = True
            if order["order"] == "ascending":
                is_sorted = all(
                    [
                        values_order[i] <= values_order[i + 1]
                        for i in range(len(values_order) - 1)
                    ]
                )
            elif order["order"] == "descending":
                is_sorted = all(
                    [
                        values_order[i] >= values_order[i + 1]
                        for i in range(len(values_order) - 1)
                    ]
                )

        if not is_sorted:
            return False, "Doesn't sort."
        else:
            return True, "Sorted."
    else:
        return True, "No sort."
