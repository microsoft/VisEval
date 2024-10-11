# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.


from pathlib import Path

import pytest

from viseval.check import surface_form_check

folder = Path(__file__).resolve().parent

def test_valid_empty():
    with open(folder / "assets/empty_3.svg", "r") as f:
        svg_string = f.read()
        answer, msg = surface_form_check(svg_string)
        assert answer == False
        
        
def test_valid_empty():
    with open(folder / "assets/pie_4_0.svg", "r") as f:
        svg_string = f.read()
        answer, msg = surface_form_check(svg_string)
        assert answer == True