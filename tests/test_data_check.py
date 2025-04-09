# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import json
from pathlib import Path

import pytest

from viseval.check import data_check, deconstruct

folder = Path(__file__).resolve().parent

with open(folder / "assets/samples.json") as f:
    benchmark = json.load(f)


def test_data_check_pie_5():
    with open(folder / "assets/pie_5.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["3264"]["vis_obj"]
        query_meta = benchmark["3264"]["query_meta"]
        result = data_check(
            chart_info, ground_truth, query_meta[0]["channel_specified"]
        )
        assert result[0] is True
        
def test_data_check_pie_4():
    with open(folder / "assets/pie_4_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["4"]["vis_obj"]
        query_meta = benchmark["4"]["query_meta"]
        result = data_check(
            chart_info, ground_truth, query_meta[0]["channel_specified"]
        )
        assert result[0] is True


def test_data_check_scatter_400():
    for i in range(2):
        with open(folder / f"assets/scatter_400_{i}.svg", "r") as f:
            svg_string = f.read()
            chart_info, msg = deconstruct(svg_string)
            ground_truth = benchmark["400"]["vis_obj"]
            query_meta = benchmark["400"]["query_meta"]
            result = data_check(
                chart_info, ground_truth, query_meta[i]["channel_specified"]
            )
            assert result[0] is True


def test_data_check_bar_1129():
    for i in range(3):
        with open(folder / f"assets/bar_1129_{i}.svg", "r") as f:
            svg_string = f.read()
            chart_info, msg = deconstruct(svg_string)
            ground_truth = benchmark["1129"]["vis_obj"]
            query_meta = benchmark["1129"]["query_meta"]
            result = data_check(
                chart_info, ground_truth, query_meta[i]["channel_specified"]
            )
            assert result[0] is True


def test_data_check_bar_2750():
    for i in range(2):
        with open(folder / f"assets/stacked_bar_2750_{i}.svg", "r") as f:
            svg_string = f.read()
            chart_info, msg = deconstruct(svg_string)
            ground_truth = benchmark["2750"]["vis_obj"]
            query_meta = benchmark["2750"]["query_meta"]
            result = data_check(
                chart_info, ground_truth, query_meta[i]["channel_specified"]
            )
            assert result[0] is True


def test_data_check_line_3240():
    with open(folder / "assets/line_3240_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["3240"]["vis_obj"]
        query_meta = benchmark["3240"]["query_meta"]
        result = data_check(
            chart_info, ground_truth, query_meta[0]["channel_specified"]
        )
        assert result[0] is True


def test_data_check_line_2781():
    with open(folder / "assets/grouping_line_2781_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["2781"]["vis_obj"]
        query_meta = benchmark["2781"]["query_meta"]
        result = data_check(
            chart_info, ground_truth, query_meta[0]["channel_specified"]
        )
        assert result[0] is False


def test_data_check_line_773():
    # yyyy-mm-dd
    with open(folder / "assets/line_773_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["773@x_name@DESC"]["vis_obj"]
        query_meta = benchmark["773@x_name@DESC"]["query_meta"]
        result = data_check(
            chart_info, ground_truth, query_meta[0]["channel_specified"]
        )
        assert result[0] is True


def test_data_check_bar_68():
    # monday - mon
    with open(folder / "assets/bar_68_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["68"]["vis_obj"]
        query_meta = benchmark["68"]["query_meta"]
        result = data_check(
            chart_info, ground_truth, query_meta[0]["channel_specified"]
        )
        assert result[0] is True


def test_data_check_bar_1071():
    # horizontal bar
    with open(folder / "assets/bar_1071_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["1071"]["vis_obj"]
        query_meta = benchmark["1071"]["query_meta"]
        result = data_check(
            chart_info, ground_truth, query_meta[0]["channel_specified"]
        )
        assert result[0] is True

        result = data_check(chart_info, ground_truth, ["x", "y"])
        assert result[0] is False


def test_data_check_bar_3137():
    # error cases
    with open(folder / "assets/bar_3137_1.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["3137@y_name@DESC"]["vis_obj"]
        query_meta = benchmark["3137@y_name@DESC"]["query_meta"]
        result = data_check(
            chart_info, ground_truth, query_meta[0]["channel_specified"]
        )
        assert result[0] is False
