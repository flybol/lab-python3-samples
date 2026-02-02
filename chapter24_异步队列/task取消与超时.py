import asyncio


async def long_job():
    try:
        print("开始 long_job")
        await asyncio.sleep(5)
        print("结束 long_job")
    except asyncio.CancelledError:
        print("long_job 被取消")
        # 在协程内部最好捕获一下 CancelledError 做清理，然后再抛出去。
        raise


async def main():
    task = asyncio.create_task(long_job())
    await asyncio.sleep(2)
    print("主协程：不想等了，取消任务")
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("主协程：确认任务已被取消")


asyncio.run(main())
