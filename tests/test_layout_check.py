# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import csv
from pathlib import Path

import pytest

from viseval.check import layout_check

folder = Path(__file__).resolve().parent

webdriver_path = "/usr/bin/chromedriver"


def test_layout_check():
    with open(folder / "assets/readability/145@y_name@DESC.svg", "r") as svg_file:
        svg_string = svg_file.read()
    assert layout_check({"svg_string": svg_string}, webdriver_path) == (
        False,
        "Overflow detected.",
    )


def test_layout_check_2():
    with open(folder / "assets/readability/2350.svg", "r") as svg_file:
        svg_string = svg_file.read()
    assert layout_check({"svg_string": svg_string}, webdriver_path) == (
        True,
        "No overflow or overlap detected.",
    )


def test_layout_check_3():
    with open(folder / "assets/readability/2652.svg", "r") as svg_file:
        svg_string = svg_file.read()
    assert layout_check({"svg_string": svg_string}, webdriver_path) == (
        False,
        "Overflow detected.",
    )


def test_layout_check_batch():
    with open(folder / "assets/readability/readability_human_rating.csv") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            svg_id = row[0]

        with open(folder / f"assets/readability/{svg_id}.svg", "r") as svg_file:
            svg_string = svg_file.read()
            print(svg_id)
        assert not layout_check({"svg_string": svg_string}, webdriver_path)[0] == (
            False if row[5] == "FALSE" else True
        )
