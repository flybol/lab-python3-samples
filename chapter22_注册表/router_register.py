from typing import Callable, Dict, Any, Awaitable

"""
Web 路由 / API 自动注册
"""

RouterHandler = Callable[..., Awaitable[Any]]

# 路由表
_ROUTES: list[tuple[str, str, RouterHandler]] = []


def route(method: str, path: str):
    def wrapper(func: RouterHandler) -> RouterHandler:
        _ROUTES.append((method, path, func))
        return func

    return wrapper


def get_routes() -> list[tuple[str, str, RouterHandler]]:
    return _ROUTES


# 业务模块

# user_api.py


@route("GET", "/users")
async def list_users(): ...


@route("POST", "/users")
async def create_user(): ...


print(get_routes())
