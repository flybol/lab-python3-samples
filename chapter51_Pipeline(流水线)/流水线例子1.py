from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Protocol, Callable, runtime_checkable


@dataclass
class Context:
    """流水线的‘工件’，所有步骤都在它上面读写数据"""

    data: dict[str, Any]


@runtime_checkable
class Step(Protocol):
    """流水线步骤接口"""

    """每个步骤都要实现 run(ctx) -> ctx"""

    def run(self, ctx: Context) -> Context: ...


class Pipeline:
    """流水线"""

    """流水线由步骤组成，每个步骤按顺序执行"""

    def __init__(self, steps: list[Step]):
        self.steps = steps

    def run(self, ctx: Context) -> Context:
        for step in self.steps:
            ctx = step.run(ctx)
        return ctx


##步骤
class AddUser:
    """添加用户"""

    def run(self, ctx: Context) -> Context:
        ctx.data["user"] = {"name": "张三", "age": 18}
        return ctx


class ValidateAge:
    def run(self, ctx: Context) -> Context:
        age = ctx.data["user"]["age"]
        if age < 0:
            raise ValueError("年龄不合法")
        return ctx


class MakeGreeting:
    def run(self, ctx: Context) -> Context:
        name = ctx.data["user"]["name"]
        ctx.data["greeting"] = f"你好，{name}！"
        return ctx


p = Pipeline([AddUser(), ValidateAge(), MakeGreeting()])
out = p.run(Context(data={}))
print(out.data)
