# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from unittest.mock import Mock

from examples.agent.coml4vis import read_table


def test_read_table_without_dynamic_execution(monkeypatch):
    dataset = object()
    read_csv = Mock(return_value=dataset)
    describe_variable = Mock(return_value={"summary": "ok"})
    monkeypatch.setattr("examples.agent.coml4vis.pd.read_csv", read_csv)
    monkeypatch.setattr(
        "examples.agent.coml4vis.describe_variable", describe_variable
    )

    code, variable_description = read_table("sales", "/tmp/data.csv", "coml")

    assert code == "sales_dataset = pd.read_csv('/tmp/data.csv')"
    assert variable_description == {"sales_dataset": {"summary": "ok"}}
    read_csv.assert_called_once_with("/tmp/data.csv")
    describe_variable.assert_called_once_with(
        dataset,
        dataframe_format="coml",
        pandas_description_config={"max_rows": 10},
    )