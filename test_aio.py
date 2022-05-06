# coding=utf-8
import asyncio
import time
from threading import Thread

import aiohttp


# 目标协程
async def run():
    print("start get:")
    print(time.time())
    res = await get()
    print("finish get:")
    print(time.time())


# 异步请求
async def get():
    url = 'http://www.baidu.com'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # return await response.read()
            return await asyncio.sleep(2)  # 假设请求返回时间


async def create_task(event_loop):
    while True:
        asyncio.run_coroutine_threadsafe(run(), event_loop)
        # 每间隔1s执行一次run()协程
        await asyncio.sleep(1)  # 设置定时时间


# 启动一个loop
def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == '__main__':
    thread_loop = asyncio.new_event_loop()  # 子线程loop
    run_loop_thread = Thread(target=start_loop, args=(thread_loop,))
    run_loop_thread.start()

    main_loop = asyncio.new_event_loop()
    main_loop.run_until_complete(create_task(thread_loop))  # 在主线程loop里面执行子线程loop
