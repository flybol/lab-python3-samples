from typing import Any, Callable, Dict

# 注册表
_COMMANDS: Dict[str, Callable[..., Any]] = {}


def register_command(name: str):
    """装饰器：把函数注册到 COMMANDS 表里"""

    def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        """装饰器内部函数"""
        _COMMANDS[name] = func  # ✅ 关键：定义时登记
        return func

    return wrapper


def get_command(name: str) -> Callable[..., Any]:
    """从注册表里获取命令"""
    return _COMMANDS[name]


# 业务代码
@register_command("login")
def login_handler(payload: Dict[str, Any]):
    print(f"开始处理登录任务：{payload}")


@register_command("publish_articles")
def publish_articles(payload: Dict[str, Any]):
    print(f"开始发布文章：{payload}")


# 这里冗余，封装一下
# login_cmd = get_command("login")
# login_cmd(payload={"username": "test", "password": "password"})

# publish_article_cmd = get_command("publish_articles")
# publish_article_cmd(payload={"title": "test", "content": "content"})

# “登记”和“查表”的基本套路


def run_cmd(name: str, playload: Dict[str, Any]):
    cmd = get_command(name)
    return cmd(playload)


run_cmd("login", {"username": "test", "password": "password"})
run_cmd("publish_articles", {"title": "test", "content": "content"})
