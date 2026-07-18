# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from importlib import import_module

__all__ = ["Chat2vis", "CoML4VIS", "Lida"]

_AGENT_MODULES = {
    "Chat2vis": ".chat2vis",
    "CoML4VIS": ".coml4vis",
    "Lida": ".lida",
}


def __getattr__(name: str):
    if name not in _AGENT_MODULES:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(_AGENT_MODULES[name], __name__)
    return getattr(module, name)
