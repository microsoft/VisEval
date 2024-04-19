import pytest
import json

from viseval.check import deconstruct, chart_check

from pathlib import Path

folder = Path(__file__).resolve().parent

with open(folder / "assets/samples.json") as f:
    benchmark = json.load(f)


def test_chart_check_pie_4():
    with open(folder / "assets/pie_4_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["4"]["vis_obj"]
        ground_truth["chart"] = benchmark["4"]["chart"]
        query_meta = benchmark["4"]["query_meta"]
        result = chart_check(
            chart_info,
            ground_truth,
            query_meta[0]["stacked_bar"] if "stacked_bar" in query_meta[0] else None,
        )
        assert result[0] is True


def test_chart_check_scatter_400():
    for i in range(2):
        with open(folder / f"assets/scatter_400_{i}.svg", "r") as f:
            svg_string = f.read()
            chart_info, msg = deconstruct(svg_string)
            ground_truth = benchmark["400"]["vis_obj"]
            ground_truth["chart"] = benchmark["400"]["chart"]
            query_meta = benchmark["400"]["query_meta"]
            result = chart_check(
                chart_info,
                ground_truth,
                (
                    query_meta[i]["stacked_bar"]
                    if "stacked_bar" in query_meta[i]
                    else None
                ),
            )
            assert result[0] is True


def test_chart_check_bar_1129():
    for i in range(3):
        with open(folder / f"assets/bar_1129_{i}.svg", "r") as f:
            svg_string = f.read()
            chart_info, msg = deconstruct(svg_string)
            ground_truth = benchmark["1129"]["vis_obj"]
            ground_truth["chart"] = benchmark["1129"]["chart"]
            query_meta = benchmark["1129"]["query_meta"]
            result = chart_check(
                chart_info,
                ground_truth,
                (
                    query_meta[i]["stacked_bar"]
                    if "stacked_bar" in query_meta[i]
                    else None
                ),
            )
            assert result[0] is True


def test_chart_check_bar_2750():
    for i in range(2):
        with open(folder / f"assets/stacked_bar_2750_{i}.svg", "r") as f:
            svg_string = f.read()
            chart_info, msg = deconstruct(svg_string)
            ground_truth = benchmark["2750"]["vis_obj"]
            ground_truth["chart"] = benchmark["2750"]["chart"]
            query_meta = benchmark["2750"]["query_meta"]
            result = chart_check(
                chart_info,
                ground_truth,
                (
                    query_meta[i]["stacked_bar"]
                    if "stacked_bar" in query_meta[i]
                    else None
                ),
            )
            assert result[0] is True


def test_chart_check_line_3240():
    with open(folder / f"assets/line_3240_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["3240"]["vis_obj"]
        ground_truth["chart"] = benchmark["3240"]["chart"]
        query_meta = benchmark["3240"]["query_meta"]
        result = chart_check(
            chart_info,
            ground_truth,
            query_meta[0]["stacked_bar"] if "stacked_bar" in query_meta[0] else None,
        )
        assert result[0] is True


def test_chart_check_line_2781():
    with open(folder / f"assets/grouping_line_2781_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["2781"]["vis_obj"]
        ground_truth["chart"] = benchmark["2781"]["chart"]
        query_meta = benchmark["2781"]["query_meta"]
        result = chart_check(
            chart_info,
            ground_truth,
            query_meta[0]["stacked_bar"] if "stacked_bar" in query_meta[0] else None,
        )
        assert result[0] is True


def test_chart_check_bar_1071():
    # horizontal bar
    with open(folder / f"assets/bar_1071_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        ground_truth = benchmark["1071"]["vis_obj"]
        ground_truth["chart"] = benchmark["1071"]["chart"]
        query_meta = benchmark["1071"]["query_meta"]
        result = chart_check(
            chart_info,
            ground_truth,
            query_meta[0]["stacked_bar"] if "stacked_bar" in query_meta[0] else None,
        )
        assert result[0] is True


def test_stacked():
    result = chart_check({"chart": "grouping bar"}, {"chart": "Stacked Bar"}, True)
    assert result[0] is False

    result = chart_check({"chart": "grouping bar"}, {"chart": "Stacked Bar"}, False)
    assert result[0] is True
