from __future__ import annotations
import yaml
import asyncio
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol


# ========= 0) Context：Pipeline 的上下文 =========
@dataclass
class PipelineContext:
    data: dict[str, Any] = field(default_factory=dict)


# ========= 1) Command：统一接口 =========
class Command(Protocol):
    async def run(self, ctx: PipelineContext) -> PipelineContext: ...


# ========= 2) Registry：type -> factory(cfg) =========
CommandFactory = Callable[[dict[str, Any]], Command]
REGISTRY: dict[str, CommandFactory] = {}


def register(step_type: str) -> Callable[[CommandFactory], CommandFactory]:
    """注册一个 step_type 对应的 Command 工厂函数"""

    def deco(factory: CommandFactory) -> CommandFactory:
        if step_type in REGISTRY:
            raise KeyError(f"Duplicate step type: {step_type}")
        REGISTRY[step_type] = factory
        return factory

    return deco


# ========= 3) 变量渲染：支持 ${key} 从 ctx.data 取 =========
_var_pat = re.compile(r"\$\{([a-zA-Z_]\w*)\}")


def render(value: Any, ctx: PipelineContext) -> Any:
    """只做最基础的渲染：str 里的 ${key} 替换为 ctx.data[key]"""
    if not isinstance(value, str):
        return value

    def repl(m: re.Match[str]) -> str:
        key = m.group(1)
        return str(ctx.data.get(key, ""))

    return _var_pat.sub(repl, value)


# ========= 4) Runner：把 steps 逐个执行 =========
async def run_pipeline(
    pcfg: dict[str, Any], ctx: PipelineContext | None = None
) -> PipelineContext:
    ctx = ctx or PipelineContext()

    steps = pcfg.get("steps", [])
    if not isinstance(steps, list):
        raise TypeError("pipeline.steps must be a list")

    for i, step_cfg in enumerate(steps, start=1):
        if not isinstance(step_cfg, dict):
            raise TypeError(f"step #{i} must be a dict")

        step_type = step_cfg.get("type")
        if not step_type:
            raise ValueError(f"step #{i} missing 'type'")

        factory = REGISTRY.get(step_type)
        if not factory:
            raise ValueError(f"Unknown step type: {step_type} (step #{i})")

        cmd = factory(step_cfg)

        # 执行前：对 step_cfg 中常用字段做渲染（你也可以选择在 Command 内部渲染）
        # 这里不强行全字段深度渲染，保持简单：各命令需要渲染的字段自己 render()
        ctx = await cmd.run(ctx)

    return ctx


# ========= 5) 内置几个最常用的基础命令 =========
@register("log")
def make_log(cfg: dict[str, Any]) -> Command:
    msg = cfg.get("message", "")

    class Log:
        async def run(self, ctx: PipelineContext) -> PipelineContext:
            print(render(msg, ctx))
            return ctx

    return Log()


@register("set")
def make_set(cfg: dict[str, Any]) -> Command:
    key = cfg["key"]
    value = cfg.get("value")

    class SetValue:
        async def run(self, ctx: PipelineContext) -> PipelineContext:
            ctx.data[key] = render(value, ctx)
            return ctx

    return SetValue()


@register("sleep")
def make_sleep(cfg: dict[str, Any]) -> Command:
    seconds = float(cfg.get("seconds", 1))

    class Sleep:
        async def run(self, ctx: PipelineContext) -> PipelineContext:
            await asyncio.sleep(seconds)
            return ctx

    return Sleep()


def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


async def main():
    pcfg = load_yaml("./chapter51_Pipeline(流水线)/pipeline.yaml")
    ctx = PipelineContext()
    await run_pipeline(pcfg, ctx)
    print("ctx.data =", ctx.data)


if __name__ == "__main__":
    asyncio.run(main())
