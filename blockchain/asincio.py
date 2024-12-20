import asyncio
import time


async def greet(name, delay):
    await asyncio.sleep(delay)
    print(f"name = {name}: delay = {delay}s")


async def main():
    task_1 = asyncio.create_task(greet("volodya", 3))
    task_2 = asyncio.create_task(greet("fedya", 2))
    task_3 = asyncio.create_task(greet("kira", 2))

    start_time = time.time()

    print("0.00s: start")
    await task_1
    await task_2
    await task_3
    print(f"{time.time() - start_time:.2f}s: finish")

asyncio.run(main())
