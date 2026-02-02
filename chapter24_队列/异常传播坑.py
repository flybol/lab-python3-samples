import asyncio


async def bad():
    raise ValueError("出错啦")


async def main():
    t = asyncio.create_task(bad())
    # 如果你从来不 await t，这个异常会在日志里以 “未处理异常” 的形式冒出来
    await asyncio.sleep(1)


asyncio.run(main())
