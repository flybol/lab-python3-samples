from yaml import safe_load as load


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return load(f)


steps_configs = read_file("./chapter51_Pipeline(流水线)/pipeline.yml")
print(f"读取文件内容：{steps_configs}")


class Registry:
    def __init__(self) -> None:
        self._items = {}

    def register(self, name: str, cls):
        self._items[name] = cls

    def create(self, name: str, **kwargs):
        cls = self._items[name]
        return cls(**kwargs)


class PrintStep:
    def run(self, ctx):
        print(f"开始执行步骤：{self.__class__.__name__}")
        print(f"步骤参数：{ctx}")
        return ctx


def build_steps(step_configs):
    steps = []
    register = Registry()

    for step_cfg in step_configs:
        print(f"开始解析步骤：{step_cfg},{step_cfg.get('with', {})}")

        step = register.create(step_cfg["uses"])
        steps.append(step)
    return steps


steps = build_steps(steps_configs["steps"])
print(f"解析构建步骤：{steps}")
