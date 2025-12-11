# handlers/user_commands.py
from command_registry import command


@command("user.create")
def create_user(payload: dict): ...


@command("user.disable")
def disable_user(payload: dict): ...
