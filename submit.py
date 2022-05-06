import time
from re import A
from turtle import pen

import pendulum
import requests
from rich import print
from get_status import check_bm_status
from get_info import check_court_status


def submit(
    token: str = "",
    cookie="",
    sports: str = "bm",
    day: str = "tomorrow",
    court_1: str = "1",
    book_time_1_1: str = "8",
    book_time_1_2: str = "9",
    court_2: str = "2",
    book_time_2_1: str = "8",
    book_time_2_2: str = "9",
):
    """
    pingpang 33 badminton 34
    badminton
    场次
    1   2   3   4   5   6   7   8   9   10  11  12
    155 156 157 158 159 160 161 162 163 164 165 166
    time 7-8    8-9    9-10   10-11  11-12  12-13  13-14  14-15
    time 328101 328102 328103 328104 328105 328106 328107
    time max 2

    pingpang
    1   2   3   4   5   6   7   8   9   10
    145 146 147 148 149 150 151 152 153 154
    time 7-8    8-9    9-10   10-11  11-12  12-13  13-14
    time 328094 328095 328096 328097 328098 328099 328100
    time max 2
    """

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

    # first group
    if sports == "bm":
        sport_events_id = "34"
    elif sports == "pp":
        sport_events_id = "33"

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

    # head
    # token ae1660ad-042d-4293-b4e8-6706a314b5ee
    if token == "":
        token = "ae1660ad-042d-4293-b4e8-6706a314b5ee"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50",
        "token": token,
        "Host": "gym.dazuiwl.cn",
        "Origin": "http://gym.dazuiwl.cn",
        "Referer": "http://gym.dazuiwl.cn/h5/",
        "Proxy-Connection": "keep-alive",
    }

    # cookies
    # cookie PHPSESSID=7a8lr0vgpbhuo8loi99uuce76j

    if cookie == "":
        cookie = {"PHPSESSID": "392enpsjdnre0svp25m8e31cmm"}

    # NOTE check cookies & token
    try:
        res = requests.post(submit_url, headers=headers, data=payload_1, cookies=cookie, timeout=5).json()
    except:
        print("please change cookie and token")
        return 0

    # NOTE check courts
    try:
        status_1 = check_court_status(
            day=day, court=court_1, book_time_1=book_time_1_1, book_time_2=book_time_1_2, print_info=True
        )
        if status_1 != 1:
            return 0
        status_2 = check_court_status(
            day=day, court=court_2, book_time_1=book_time_2_1, book_time_2=book_time_2_2, print_info=True
        )
        if status_2 != 1:
            return 0
    except:
        print("check field")
        return 0

    today = pendulum.today().to_date_string()
    over_time = pendulum.parser.parse(today + "T07:20:00+08:00")
    begin_time = pendulum.parser.parse(today + "T06:59:55+08:00")
    flag = 0

    while True:
        # Time judge
        now = pendulum.now()
        print(":timer_clock: ", now)

        if now >= begin_time:

            # TODO 异步
            """
            从6:59:55开始到7:20开始, async 异步实现同时发出200个左右的请求, 每个场地请求100次
            需要记录一下单词api时间, timeout很重要, 要保持和服务器的连接
            """

            try:
                res_1 = requests.post(submit_url, headers=headers, data=payload_1, cookies=cookie, timeout=10).json()
                res_2 = requests.post(submit_url, headers=headers, data=payload_2, cookies=cookie, timeout=10).json()
                if res_1["code"] == 1 or res_2["code"] == 1:
                    flag = 1
                    break
                pass

            except:
                print("try again")
        else:
            time.sleep(0.5)

        if now >= over_time:
            break

    if flag == 1:
        print(":rocket: success")
        return 1
    else:
        print(":loudly_crying_face: field")
        return 0


if __name__ == "__main__":
    submit(
        sports="bm",
        day="tomorrow",
        court_1="1",
        book_time_1_1="10",
        book_time_1_2="11",
        court_2="2",
        book_time_2_1="10",
        book_time_2_2="11",
    )
