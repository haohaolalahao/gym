import asyncio
import random
import time
from threading import Thread
from turtle import pen

import aiohttp
import pendulum
import requests
from rich import print

from get_info import check_court_status
from get_status import check_bm_status


async def fetch(session, url, payload):
    async with session.post(url, data=payload) as resp:
        # if resp.status != 200:
        #     resp.raise_for_status()
        data = await resp.json()
        # for test
        # await asyncio.sleep(2)
        print(pendulum.now(), data)
        if data["code"] == 1:
            for i in range(10):
                print("[bold red]SUCCESS !")
        return data["code"]


async def fetch_multi(session, url, payloads):
    tasks = []
    for payload in payloads:
        task = asyncio.create_task(fetch(session, url, payload))
        tasks.append(task)
    # gather: 搜集所有future对象，并等待返回
    results = await asyncio.gather(*tasks)
    return results


async def post_main(url: str, payloads: list, headers: dict, cookies: dict):
    # tcp 连接池
    connection = aiohttp.TCPConnector(limit=10)
    timeout = aiohttp.ClientTimeout(total=300, connect=60, sock_connect=60, sock_read=60)
    async with aiohttp.ClientSession(
        headers=headers, cookies=cookies, connector=connection, timeout=timeout
    ) as session:
        res = await fetch_multi(session, url, payloads)
        return res


# 目标协程
async def run(url: str, payloads: list, headers: dict, cookies: dict):
    print("Start: ", pendulum.now())
    res = await post_main(url, payloads, headers, cookies)
    # print(res)
    # if 0 in res:
    #     print('hello world')
    #     raise Exception("Error")
    print("End: ", pendulum.now())


# async def get():
#     url = 'http://www.baidu.com'
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             # return await response.read()
#             return await asyncio.sleep(2)  # 假设请求返回时间


async def create_task(event_loop, url: str, payloads: list, headers: dict, cookies: dict, endtime):
    time_flag = True
    while time_flag:
        time_flag = pendulum.now() < endtime
        asyncio.run_coroutine_threadsafe(run(url, payloads, headers, cookies), event_loop)
        await asyncio.sleep(random.random())
    print("[bold red]End asyncio loop")


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def submit(
    token: str = "",
    cookie="",
    day: str = "tomorrow",
    court_1: str = "1",
    book_time_1_1: str = "8",
    book_time_1_2: str = "9",
    court_2: str = "2",
    book_time_2_1: str = "8",
    book_time_2_2: str = "9",
):
    # pay
    submit_url = "http://gym.dazuiwl.cn/api/order/submit"

    courts = ["155", "156", "157", "158", "159", "160", "161", "162", "163", "164", "165", "166"]
    court_times = [
        "328101",
        "328102",
        "328103",
        "328104",
        "328105",
        "328106",
        "328107",
        "328125",
        "328126",
        "328127",
        "328128",
        "328129",
        "328130",
        "328131",
        "328132",
    ]

    sport_events_id = "34"

    # NOTE money needn't change

    money = "10"

    # TODO check day
    if day == "today":
        day = pendulum.today().to_date_string()
    elif day == "tomorrow":
        day = pendulum.tomorrow().to_date_string()
    else:
        pass

    # first group
    court_index_1 = int(eval(court_1))
    assert 1 <= court_index_1 <= 12, "bad court number"
    book_time_index_1_1 = int(eval(book_time_1_1))
    assert 7 <= book_time_index_1_1 <= 21, "bad book time first"

    if book_time_1_2 == "":
        book_time_index_1_2 = False
    else:
        book_time_index_1_2 = int(eval(book_time_1_2))
        assert 7 <= book_time_index_1_2 <= 21, "bad book time second"

    court_real_1 = courts[court_index_1 - 1]
    if book_time_index_1_2:
        book_time_1 = court_times[book_time_index_1_1 - 7] + ", " + court_times[book_time_index_1_2 - 7]
    else:
        book_time_1 = court_times[book_time_index_1_1 - 7]
    scene_1 = '[{"day":"' + f"{day}" + '","fields":{"' + f"{court_real_1}" + '":[' + f"{book_time_1}" + "]}}]"
    payload_1 = {
        "orderid": "",
        "card_id": "",
        "sport_events_id": sport_events_id,
        "money": money,
        "ordertype": "makeappointment",
        "paytype": "bitpay",
        "scene": scene_1,
        "openid": "",
    }

    # second group
    court_index_2 = int(eval(court_2))
    assert 1 <= court_index_2 <= 12, "bad court number"
    book_time_index_2_1 = int(eval(book_time_2_1))
    assert 7 <= book_time_index_2_1 <= 21, "bad book time first"

    if book_time_2_2 == "":
        book_time_index_2_2 = False
    else:
        book_time_index_2_2 = int(eval(book_time_2_2))
        assert 7 <= book_time_index_2_2 <= 21, "bad book time second"

    court_real_2 = courts[court_index_2 - 1]
    if book_time_index_2_2:
        book_time_2 = court_times[book_time_index_2_1 - 7] + ", " + court_times[book_time_index_2_2 - 7]
    else:
        book_time_2 = court_times[book_time_index_2_1 - 7]
    scene_2 = '[{"day":"' + f"{day}" + '","fields":{"' + f"{court_real_2}" + '":[' + f"{book_time_2}" + "]}}]"
    payload_2 = {
        "orderid": "",
        "card_id": "",
        "sport_events_id": sport_events_id,
        "money": money,
        "ordertype": "makeappointment",
        "paytype": "bitpay",
        "scene": scene_2,
        "openid": "",
    }

    if token == "":
        token = "e89f930e-a05b-43c3-97d5-2485db3a1d86"

    if cookie == "":
        cookie = {"PHPSESSID": "pttndkiboourekn7dstkeaca52"}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50",
        "token": token,
        "Host": "gym.dazuiwl.cn",
        "Origin": "http://gym.dazuiwl.cn",
        "Referer": "http://gym.dazuiwl.cn/h5/",
        "Proxy-Connection": "keep-alive",
    }

    # NOTE check cookies & token
    # try:
    #     res = requests.post(submit_url,
    #                         headers=headers,
    #                         data=payload_1,
    #                         cookies=cookie,
    #                         timeout=5).json()
    # except:
    #     print("please change cookie and token")
    #     return 0

    # NOTE check courts
    # try:
    #     status_1 = check_court_status(day=day,
    #                                   court=court_1,
    #                                   book_time_1=book_time_1_1,
    #                                   book_time_2=book_time_1_2,
    #                                   print_info=True)
    #     if status_1 != 1:
    #         return 0
    #     status_2 = check_court_status(day=day,
    #                                   court=court_2,
    #                                   book_time_1=book_time_2_1,
    #                                   book_time_2=book_time_2_2,
    #                                   print_info=True)
    #     if status_2 != 1:
    #         return 0
    # except:
    #     print("check field")
    #     return 0

    today = pendulum.today().to_date_string()
    over_time = pendulum.parser.parse(today + "T07:02:00+08:00")
    begin_time = pendulum.parser.parse(today + "T06:59:59+08:00")

    while True:
        # Time judge
        now = pendulum.now()
        print(":timer_clock: ", now)

        if now >= begin_time:
            # NOTE requests
            # try:
            #     res_1 = requests.post(submit_url,
            #                           headers=headers,
            #                           data=payload_1,
            #                           cookies=cookie,
            #                           timeout=10).json()
            #     res_2 = requests.post(submit_url,
            #                           headers=headers,
            #                           data=payload_2,
            #                           cookies=cookie,
            #                           timeout=10).json()
            #     if res_1["code"] == 1 or res_2["code"] == 1:
            #         flag = 1
            #         break
            #     pass

            # except:
            #     print("try again")

            # NOTE asyncio
            thread_loop = asyncio.new_event_loop()  # 子线程loop
            run_loop_thread = Thread(target=start_loop, args=(thread_loop,))
            run_loop_thread.start()

            main_loop = asyncio.new_event_loop()
            main_loop.run_until_complete(
                create_task(
                    thread_loop,
                    url=submit_url,
                    payloads=[payload_1, payload_2],
                    headers=headers,
                    cookies=cookie,
                    endtime=over_time,
                )
            )

            main_loop.close()
            time.sleep(300)
            thread_loop.close()
            print("[bold red]Close Terminal")
            break
        else:
            pass

    print("[bold red]done")


if __name__ == "__main__":
    submit(
        # day="tomorrow",
        day="2022-05-22",
        court_1="2",
        book_time_1_1="10",
        book_time_1_2="11",
        court_2="3",
        book_time_2_1="10",
        book_time_2_2="11",
    )
