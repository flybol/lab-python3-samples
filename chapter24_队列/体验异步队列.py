import asyncio
import random


async def producer(q):
    for i in range(10):
        print(f"生产->{i}")
        await q.put(i)
        await asyncio.sleep(random.randint(1, 3) / 5)


async def consumer(q):
    while True:
        item = await q.get()
        print(f"消费->{item}")
        await asyncio.sleep(random.randint(1, 3) / 5)
        q.task_done()


async def main():
    # 创建队列
    q = asyncio.Queue()
    # 创建任务,给任务添加消费者
    asyncio.create_task(consumer(q))
    await producer(q)
    # 等待队列中的任务完成
    await q.join()


asyncio.run(main())
