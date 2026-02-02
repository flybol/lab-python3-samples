import asyncio
import random


async def call_service(name: str):
    delay = random.uniform(0.5, 2.0)
    print(f"调用 {name}，预计耗时 {delay:.2f}s")
    await asyncio.sleep(delay)
    print(f"{name} 返回")
    return f"{name}_result"


async def main():
    services = [f"service_{i}" for i in range(1, 10)]
    results = await asyncio.gather(*(call_service(s) for s in services))
    print("全部结果：", results)


asyncio.run(main())
