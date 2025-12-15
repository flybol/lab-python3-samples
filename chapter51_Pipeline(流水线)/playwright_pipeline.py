import asyncio
from dataclasses import dataclass
from playwright.async_api import Page, async_playwright, FrameLocator


@dataclass
class CrawlContext:
    # 1️⃣ Pipeline 上下文（Context）
    page: Page
    data: dict


class PWCommand:
    # 2️⃣ Command 接口
    async def run(self, ctx: CrawlContext) -> CrawlContext: ...


class NavigateCommand(PWCommand):
    # 3️⃣ 具体命令：导航
    def __init__(self, url: str):
        self.url = url

    async def run(self, ctx: CrawlContext) -> CrawlContext:
        await ctx.page.goto(self.url)
        return ctx


class ClickCommand(PWCommand):
    # 3️⃣ 具体命令：点击
    def __init__(self, selector: str):
        self.selector = selector

    async def run(self, ctx: CrawlContext) -> CrawlContext:
        await ctx.page.locator(self.selector).click()
        return ctx


class FillCommand(PWCommand):
    # 3️⃣ 具体命令：填写表单
    def __init__(self, selector: str, value: str):
        self.selector = selector
        self.value = value

    async def run(self, ctx: CrawlContext) -> CrawlContext:
        await ctx.page.locator(self.selector).fill(self.value)
        return ctx


class InFrameCommand(PWCommand):
    """🧭 将后续命令切换到 iframe 作用域执行（工程化适配 iframe 登录页）"""

    def __init__(self, iframe_selector: str, *steps: PWCommand):
        self.iframe_selector = iframe_selector
        self.steps = steps

    async def run(self, ctx: CrawlContext) -> CrawlContext:
        frame: FrameLocator = ctx.page.frame_locator(self.iframe_selector)

        # 给子命令一个“frame scoped”的执行能力：简单起见放 ctx.data
        ctx.data["_frame"] = frame

        for step in self.steps:
            ctx = await step.run(ctx)

        return ctx


class FillInFrameCommand(PWCommand):
    def __init__(self, selector: str, value: str):
        self.selector = selector
        self.value = value

    async def run(self, ctx: CrawlContext) -> CrawlContext:
        frame: FrameLocator = ctx.data["_frame"]
        await frame.locator(self.selector).fill(self.value)
        return ctx


class ClickInFrameCommand(PWCommand):
    def __init__(self, selector: str):
        self.selector = selector

    async def run(self, ctx: CrawlContext) -> CrawlContext:
        frame: FrameLocator = ctx.data["_frame"]
        await frame.locator(self.selector).click()
        return ctx


# 使用
async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        ctx = CrawlContext(page, {})
        ctx = await NavigateCommand("https://mail.126.com/").run(ctx)

        ctx = await InFrameCommand(
            "iframe[id^='x-URS-iframe']",
            FillCommand("input[name='email']", "lovelookyou"),
            FillCommand("input[name='password']", "haohao99"),
            ClickCommand("span[id='dologin']"),
        ).run(ctx)


asyncio.run(main())
