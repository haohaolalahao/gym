from http import cookies
import aiohttp
import asyncio
import pendulum

token = "ae1660ad-042d-4293-b4e8-6706a314b5ee"

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50",
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




async def main():
    async with aiohttp.ClientSession(headers=headers, cookies=cookie) as session:
        async with session.post(submit_url, data=payload) as response:
            print('1-1', pendulum.now())
            # print("Status:", response.status)
            # print("Content-type:", response.headers['content-type'])

            data = await response.json()
            print(data)
            print('1-2', pendulum.now())

        async with session.post(submit_url, data=payload_1) as response:
            print('2-1', pendulum.now())
            # print("Status:", response.status)
            # print("Content-type:", response.headers['content-type'])

            data = await response.json()
            print(data)
            print('2-2', pendulum.now())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
