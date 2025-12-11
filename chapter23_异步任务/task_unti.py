import asyncio
import time


async def worker(name: str, delay: float):
    print(f"[{time.strftime('%X')}] {name} 开始工作，预计耗时 {delay}s")
    await asyncio.sleep(delay)  # 模拟 IO 操作
    print(f"[{time.strftime('%X')}] {name} 完成")
    return f"{name} result"


async def main():
    print(f"[{time.strftime('%X')}] main 开始")

    # ✅ 把协程对象包装成 Task，挂到事件循环上
    task1 = asyncio.create_task(worker("任务A", 2))
    task2 = asyncio.create_task(worker("任务B", 3))

    # 也可以用 asyncio.gather 一次等待所有结果
    result1, result2 = await asyncio.gather(task1, task2)

    print(f"[{time.strftime('%X')}] 所有任务完成：", result1, result2)


if __name__ == "__main__":
    asyncio.run(main())
