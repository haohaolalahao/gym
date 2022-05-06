import asyncio
from http import cookies
from threading import Thread

import aiohttp
import pendulum
from rich import print

token = "ae1660ad-042d-4293-b4e8-6706a314b5ee"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50",
    "token": token,
    "Host": "gym.dazuiwl.cn",
    "Origin": "http://gym.dazuiwl.cn",
    "Referer": "http://gym.dazuiwl.cn/h5/",
    "Proxy-Connection": "keep-alive",
}

cookie = {"PHPSESSID": "392enpsjdnre0svp25m8e31cmm"}

submit_url = "http://gym.dazuiwl.cn/api/order/submit"


payload = {
    "orderid": "",
    "card_id": "",
    "sport_events_id": 34,
    "money": 10,
    "ordertype": "makeappointment",
    "paytype": "bitpay",
    "scene": '[{"day":"2022-05-07","fields":{"155":[328101]}}]',
    "openid": "",
}

payload_1 = {
    "orderid": "",
    "card_id": "",
    "sport_events_id": 34,
    "money": 10,
    "ordertype": "makeappointment",
    "paytype": "bitpay",
    "scene": '[{"day":"2022-05-07","fields":{"156":[328102]}}]',
    "openid": "",
}


async def fetch(session, url, payload):
    async with session.post(url, data=payload) as resp:
        if resp.status != 200:
            resp.raise_for_status()
        data = await resp.json()
        # for test
        # await asyncio.sleep(2)
        print(pendulum.now(), data)
        return data['code']


async def fetch_multi(session, url, payloads):
    tasks = []
    for payload in payloads:
        task = asyncio.create_task(fetch(session, url, payload))
        tasks.append(task)
    # gather: 搜集所有future对象，并等待返回
    results = await asyncio.gather(*tasks)
    return results


async def post_main():
    url = "http://gym.dazuiwl.cn/api/order/submit"
    payloads = [payload, payload_1]
    # tcp 连接池
    connection = aiohttp.TCPConnector(limit=3)
    timeout = aiohttp.ClientTimeout(total=60, connect=10, sock_connect=10, sock_read=10)
    async with aiohttp.ClientSession(headers=headers, cookies=cookie, connector=connection, timeout=timeout) as session:
        res = await fetch_multi(session, submit_url, payloads)
        return res

# 目标协程
async def run():
    print("Start: ", pendulum.now())
    res = await post_main()
    print(res)
    # if 0 in res:
    #     print('hello world')
    #     raise Exception("Error")
    print("End: ", pendulum.now())


# # 异步请求
# async def get():
#     url = 'http://www.baidu.com'
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             # return await response.read()
#             return await asyncio.sleep(2)  # 假设请求返回时间


async def create_task(event_loop):
    while True:
        asyncio.run_coroutine_threadsafe(run(), event_loop)
        # 每间隔1s执行一次run()协程
        await asyncio.sleep(0.5)  # 设置定时时间


# 启动一个loop
def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == "__main__":
    # asyncio.run(main())

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())

    thread_loop = asyncio.new_event_loop()  # 子线程loop
    run_loop_thread = Thread(target=start_loop, args=(thread_loop,))
    run_loop_thread.start()

    main_loop = asyncio.new_event_loop()
    main_loop.run_until_complete(create_task(thread_loop))  # 在主线程loop里面执行子线程loop
