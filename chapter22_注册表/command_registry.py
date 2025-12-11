# command_registry.py
from typing import Callable, Dict, Any

_COMMANDS: Dict[str, Callable[[dict], Any]] = {}


def command(name: str):
    def decorator(func: Callable[[dict], Any]) -> Callable[[dict], Any]:
        _COMMANDS[name] = func
        return func

    return decorator


def run_command(name: str, payload: dict):
    handler = _COMMANDS[name]
    return handler(payload)
