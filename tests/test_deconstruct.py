# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from pathlib import Path

import pytest

from viseval.check import deconstruct

folder = Path(__file__).resolve().parent


# error case
def test_deconstruct_empty():
    with open(folder / "assets/empty.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert len(chart_info["data"]) == 0


def test_deconstruct_empty1():
    with open(folder / "assets/empty_1.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert len(chart_info["data"]) == 0


def test_deconstruct_empty2():
    with open(folder / "assets/empty_2.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert len(chart_info["data"]) == 0


def test_deconstruct_empty3():
    with open(folder / "assets/empty_3.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info is None


def test_deconstruct_empty4():
    with open(folder / "assets/empty_4.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        print(chart_info)
        assert len(chart_info["data"]) == 0


def test_deconstruct_dual_axis():
    with open(folder / "assets/dual_1499_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info is None


def test_deconstruct_bar_error():
    with open(folder / "assets/bar_error_3227_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "bar"
        assert chart_info["chart"] == "vertical bar(error)"


def test_deconstruct_scatter():
    with open(folder / "assets/scatter.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "circle"
        assert chart_info["chart"] == "scatter"
        assert len(chart_info["encoding"].keys()) == 2
        assert (
            chart_info["title"]
            == "Correlation between IMDB Rating and Rotten Tomatoes Rating in Action Movies"
        )
        assert chart_info["encoding"]["x"]["title"] == "IMDB Rating"
        assert chart_info["encoding"]["y"]["title"] == "Rotten Tomatoes Rating"
        assert len(chart_info["data"]) == 309


def test_deconstruct_scatter1():
    with open(folder / "assets/scatter_1.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "circle"
        assert chart_info["chart"] == "scatter"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 5


def test_deconstruct_scatter2():
    with open(folder / "assets/scatter_2.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "circle"
        assert chart_info["chart"] == "scatter"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 100


def test_deconstruct_scatter4():
    with open(folder / "assets/scatter_4.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "circle"
        assert chart_info["chart"] == "scatter"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 3


def test_deconstruct_scatter6():
    with open(folder / "assets/scatter_6.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "circle"
        assert chart_info["chart"] == "scatter"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 69


def test_deconstruct_scatter_lida():
    with open(folder / "assets/scatter_62.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "circle"
        assert chart_info["chart"] == "scatter"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 9


def test_deconstruct_scatter_lida2():
    with open(folder / "assets/scatter_292.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "circle"
        assert chart_info["chart"] == "scatter"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 3


def test_deconstruct_scatter_lida3():
    with open(folder / "assets/scatter_674.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        print(chart_info)
        assert chart_info["mark"] == "circle"
        assert chart_info["chart"] == "scatter"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 76


# black legend
def test_deconstruct_grouping_scatter7():
    with open(folder / "assets/grouping_scatter_3272_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "circle"
        assert chart_info["chart"] == "grouping scatter"
        assert len(chart_info["encoding"].keys()) == 3
        assert len(chart_info["data"]) == 6


def test_deconstruct_grouping_scatter():
    with open(folder / "assets/grouping_scatter.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "circle"
        assert chart_info["chart"] == "grouping scatter"
        assert len(chart_info["encoding"].keys()) == 3
        assert len(chart_info["data"]) == 5


def test_deconstruct_line():
    with open(folder / "assets/line.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "line"
        assert chart_info["chart"] == "line"
        assert len(chart_info["encoding"].keys()) == 2
        assert chart_info["title"] == "Maximum Temperature by Month"
        assert chart_info["encoding"]["x"]["title"] == "Month"
        assert chart_info["encoding"]["y"]["title"] == "Temperature (°C)"
        assert len(chart_info["data"]) == 12


def test_deconstruct_line1():
    with open(folder / "assets/line_1.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "line"
        assert chart_info["chart"] == "line"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 20


def test_deconstruct_line2():
    with open(folder / "assets/line_2.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "line"
        assert chart_info["chart"] == "line"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 107


def test_deconstruct_line3():
    with open(folder / "assets/line_3.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "line"
        assert chart_info["chart"] == "line"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 10


def test_deconstruct_line4():
    with open(folder / "assets/line_4.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "line"
        assert chart_info["chart"] == "line"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 107


# error case
def test_deconstruct_line5():
    with open(folder / "assets/line_5.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "line"
        assert chart_info["chart"] == "line"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 0


# error case
def test_deconstruct_line11():
    with open(folder / "assets/line_11.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert "mark" not in chart_info


# tick line
def test_deconstruct_line12():
    with open(folder / "assets/line_12.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "line"
        assert chart_info["chart"] == "line"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 13


def test_deconstruct_line13():
    with open(folder / "assets/line_13.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "line"
        assert chart_info["chart"] == "line"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 15


def test_deconstruct_line14():
    with open(folder / "assets/line_1746_1.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "circle"
        assert chart_info["chart"] == "scatter"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 1


def test_deconstruct_grouping_line():
    with open(folder / "assets/grouping_line.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "line"
        assert chart_info["chart"] == "grouping line"
        assert len(chart_info["encoding"].keys()) == 3
        assert len(chart_info["data"]) == 9


def test_deconstruct_grouping_line1():
    with open(folder / "assets/grouping_line_1.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "line"
        assert chart_info["chart"] == "grouping line"
        assert len(chart_info["encoding"].keys()) == 3
        assert len(chart_info["data"]) == 20


def test_deconstruct_grouping_line4():
    with open(folder / "assets/grouping_line_4.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert len(chart_info["encoding"].keys()) == 2


# error case
def test_deconstruct_grouping_line2():
    with open(folder / "assets/grouping_line_2.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "line"
        assert chart_info["chart"] == "grouping line"
        assert len(chart_info["encoding"].keys()) == 3
        assert len(chart_info["data"]) == 0


def test_deconstruct_grouping_line3():
    with open(folder / "assets/grouping_line_3.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "line"
        assert chart_info["chart"] == "grouping line"
        assert len(chart_info["encoding"].keys()) == 3
        assert len(chart_info["data"]) == 0


def test_deconstruct_bar():
    with open(folder / "assets/bar.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "bar"
        assert chart_info["chart"] == "vertical bar"
        assert len(chart_info["encoding"].keys()) == 2
        assert chart_info["title"] == "Number of Students Advised by Faculty Rank"
        assert chart_info["encoding"]["x"]["title"] == "Faculty Rank"
        assert chart_info["encoding"]["y"]["title"] == "Number of Students Advised"
        assert len(chart_info["data"]) == 3


def test_deconstruct_bar1():
    with open(folder / "assets/bar_1.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "bar"
        assert chart_info["chart"] == "horizontal bar"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 7


def test_deconstruct_bar6():
    with open(folder / "assets/bar_6.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "bar"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 49


# 1 bar
def test_deconstruct_bar7():
    with open(folder / "assets/bar_2733_0.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "bar"
        assert chart_info["chart"] == "horizontal bar"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 1


# bar legend error
def test_deconstruct_bar8():
    with open(folder / "assets/stacked_bar_2815.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "bar"
        assert len(chart_info["encoding"].keys()) == 2


def test_deconstruct_bar9():
    with open(folder / "assets/bar_186.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "bar"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 14


def test_deconstruct_bar10():
    with open(folder / "assets/bar_3269.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "bar"
        assert len(chart_info["encoding"].keys()) == 2
        print(chart_info)
        assert len(chart_info["data"]) == 6


# lida bar
def test_deconstruct_bar_lida1():
    with open(folder / "assets/bar_9.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "bar"
        assert chart_info["chart"] == "vertical bar"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 4


# lida bar
def test_deconstruct_bar_lida2():
    with open(folder / "assets/bar_205.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "bar"
        assert chart_info["chart"] == "vertical bar"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 2


def test_deconstruct_stacked_bar():
    with open(folder / "assets/stacked_bar.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "bar"
        assert chart_info["chart"] == "vertical stacked bar"
        assert len(chart_info["encoding"].keys()) == 3
        assert chart_info["title"] == "Faculty by Rank/Sex"
        assert chart_info["encoding"]["x"]["title"] == "Rank"
        assert chart_info["encoding"]["y"]["title"] == "Number of faculty"
        assert len(chart_info["data"]) == 7


def test_deconstruct_stacked_bar1():
    with open(folder / "assets/stacked_bar_1.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "bar"
        assert chart_info["chart"] == "vertical stacked bar"
        assert len(chart_info["encoding"].keys()) == 3
        assert len(chart_info["data"]) == 9


def test_deconstruct_grouping_bar():
    with open(folder / "assets/bar_189.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "bar"
        assert chart_info["chart"] == "vertical grouping bar"
        assert len(chart_info["encoding"].keys()) == 3
        assert len(chart_info["data"]) == 4


def test_deconstruct_pie():
    with open(folder / "assets/pie.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "arc"
        assert chart_info["chart"] == "pie"
        assert len(chart_info["encoding"].keys()) == 2
        assert chart_info["title"] == "Maximum Price of Each Film"
        assert len(chart_info["data"]) == 5


# 180 degree
def test_deconstruct_pie1():
    with open(folder / "assets/pie_1.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "arc"
        assert chart_info["chart"] == "pie"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 3
        flag = False
        for datum in chart_info["data"]:
            # = 50 percent
            if datum["field_theta"] == 50:
                flag = True
        assert flag


# shadow and > 180 degree
def test_deconstruct_pie2():
    with open(folder / "assets/pie_2.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "arc"
        assert chart_info["chart"] == "pie"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 3
        flag = False
        for datum in chart_info["data"]:
            # > 50 percent
            if datum["field_theta"] > 50:
                flag = True
        assert flag


# shadow and > 180 degree
def test_deconstruct_pie3():
    with open(folder / "assets/pie_3.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "arc"
        assert chart_info["chart"] == "pie"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 2
        flag = False
        for datum in chart_info["data"]:
            # > 50 percent
            if datum["field_theta"] > 50:
                flag = True
        assert flag


# 360 degree
def test_deconstruct_pie3():
    with open(folder / "assets/pie_4.svg", "r") as f:
        svg_string = f.read()
        chart_info, msg = deconstruct(svg_string)
        assert chart_info["mark"] == "arc"
        assert chart_info["chart"] == "pie"
        assert len(chart_info["encoding"].keys()) == 2
        assert len(chart_info["data"]) == 1
        flag = False
        for datum in chart_info["data"]:
            # > 50 percent
            if datum["field_theta"] == 100:
                flag = True
        assert flag
