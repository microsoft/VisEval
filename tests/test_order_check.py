import pytest
import json

from viseval.check import deconstruct, data_check, order_check

from pathlib import Path

folder = Path(__file__).resolve().parent

with open(folder / "assets/samples.json") as f:
    benchmark = json.load(f)


def test_order_check_line_773():
    # x ascending
    with open(folder / "assets/line_773_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        # yyyy-mm-dd
        ground_truth = benchmark["773@x_name@DESC"]["vis_obj"]
        query_meta = benchmark["773@x_name@DESC"]["query_meta"]
        answer, rationale = data_check(
            chart_info, ground_truth, query_meta[0]["channel_specified"]
        )

        answer, rationale = order_check(
            chart_info, ground_truth, query_meta[0]["sort_by"]
        )
        assert answer is True

        ground_truth["sort"]["order"] = "descending"
        answer, rationale = order_check(
            chart_info, ground_truth, query_meta[0]["sort_by"]
        )
        assert answer is False


def test_order_check_bar_680():
    # y descending
    with open(folder / "assets/stacked_bar_680_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["680@y_name@DESC"]["vis_obj"]
        query_meta = benchmark["680@y_name@DESC"]["query_meta"]
        answer, rationale = data_check(
            chart_info, ground_truth, query_meta[0]["channel_specified"]
        )

        answer, rationale = order_check(
            chart_info, ground_truth, query_meta[0]["sort_by"]
        )
        assert answer is True

        ground_truth["sort"]["order"] = "ascending"
        answer, rationale = order_check(
            chart_info, ground_truth, query_meta[0]["sort_by"]
        )
        assert answer is False


def test_order_check_bar_2815():
    # x descending
    # swap channel x-z
    with open(folder / "assets/stacked_bar_2815_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["2815@x_name@DESC"]["vis_obj"]
        query_meta = benchmark["2815@x_name@DESC"]["query_meta"]
        answer, rationale = data_check(
            chart_info, ground_truth, query_meta[0]["channel_specified"]
        )

        answer, rationale = order_check(
            chart_info, ground_truth, query_meta[0]["sort_by"]
        )
        assert answer is True

        ground_truth["sort"]["order"] = "ascending"
        answer, rationale = order_check(
            chart_info, ground_truth, query_meta[0]["sort_by"]
        )
        assert answer is False


# horizontal bar
def test_order_check_bar_2060():
    # y descending
    # swap channel x-y
    with open(folder / "assets/bar_2060_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["2060@y_name@DESC"]["vis_obj"]
        query_meta = benchmark["2060@y_name@DESC"]["query_meta"]
        answer, rationale = data_check(chart_info, ground_truth, [])

        answer, rationale = order_check(
            chart_info, ground_truth, query_meta[0]["sort_by"]
        )
        assert answer is False

        # x quantitative descending
        answer, rationale = order_check(chart_info, ground_truth, "attribute")
        assert answer is True

        ground_truth["sort"]["order"] = "ascending"
        answer, rationale = order_check(chart_info, ground_truth, "attribute")
        assert answer is False


# horizontal bar
def test_order_check_bar_1000():
    # y descending
    # swap channel x-y
    with open(folder / "assets/bar_1000_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["1000@y_name@DESC"]["vis_obj"]
        query_meta = benchmark["1000@y_name@DESC"]["query_meta"]
        answer, rationale = data_check(chart_info, ground_truth, [])
        print(answer, rationale)
        answer, rationale = order_check(
            chart_info, ground_truth, query_meta[0]["sort_by"]
        )
        assert answer is False

        # x quantitative descending
        ground_truth["sort"]["channel"] = "x"
        answer, rationale = order_check(
            chart_info, ground_truth, query_meta[0]["sort_by"]
        )
        assert answer is True

        # y nominal descending
        ground_truth["sort"]["channel"] = "y"
        chart_info["encoding"]["y"]["scale"]["domain"] = [
            "sony",
            "jcrew",
            "gucci",
            "apple",
        ]
        answer, rationale = order_check(
            chart_info, ground_truth, query_meta[0]["sort_by"]
        )
        assert answer is True

        # custom order
        ground_truth["sort"]["order"] = ["sony", "jcrew", "gucci", "apple"]
        answer, rationale = order_check(
            chart_info, ground_truth, query_meta[0]["sort_by"]
        )
        assert answer is True


# invert y axis, zero value
def test_order_check_bar_550():
    with open(folder / "assets/bar_550_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["550@y_name@DESC"]["vis_obj"]
        query_meta = benchmark["550@y_name@DESC"]["query_meta"]
        answer, rationale = data_check(
            chart_info, ground_truth, query_meta[0]["channel_specified"]
        )

        answer, rationale = order_check(
            chart_info, ground_truth, query_meta[0]["sort_by"]
        )
        assert answer is True
