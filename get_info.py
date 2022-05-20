import pendulum
import requests
from rich import print


# only for badminton
def check_court_status(
    day: str = "tomorrow", court: str = "1", book_time_1: str = "7", book_time_2: str = "", print_info: bool = True
):
    """
    this function checks the availability of a tennis court at the specified time and date.

    :param day: str = "tomorrow", defaults to tomorrow
    :type day: str (optional)
    :param court: str = '1', defaults to 1
    :type court: str (optional)
    :param book_time_1: str = '7', defaults to 7
    :type book_time_1: str (optional)
    :param book_time_2: str = '',
    :type book_time_2: str
    :param print_info: bool = True, defaults to True
    :type print_info: bool (optional)
    """
    if day == "today":
        day = pendulum.today().to_date_string()
    elif day == "tomorrow":
        day = pendulum.tomorrow().to_date_string()
    else:
        pass

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

    court_index = int(eval(court))
    assert 1 <= court_index <= 12, "bad court number"
    book_time_index_1 = int(eval(book_time_1))
    assert 7 <= book_time_index_1 <= 21, "bad book time first"

    if book_time_2 == "":
        book_time_index_2 = False
    else:
        book_time_index_2 = int(eval(book_time_2))
        assert 7 <= book_time_index_2 <= 21, "bad book time second"

    court = courts[court_index - 1]
    if book_time_index_2:
        book_time = court_times[book_time_index_1 - 7] + ", " + court_times[book_time_index_2 - 7]
    else:
        book_time = court_times[book_time_index_1 - 7]

    if print_info:
        print("[bold blue]Check time: ", day)
        print("[bold blue]Check court: ", str(court_index))
        if book_time_index_2:
            print("[bold blue]Check book time: ", str(book_time_index_1) + ", " + str(book_time_index_2))
        else:
            print("[bold blue]Check book time: ", str(book_time_index_1))

    scene = '[{"day":"' + f"{day}" + '","fields":{"' + f"{court}" + '":[' + f"{book_time}" + "]}}]"

    url = "http://gym.dazuiwl.cn/api/sport_schedule/check/id/34"

    payload = {
        "scene": scene,
    }

    # TODO change token
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50",
        "token": "0ab1d598-6d23-4d9c-a8fd-9b9aaee62b68",
        "Host": "gym.dazuiwl.cn",
        "Origin": "http://gym.dazuiwl.cn",
        "Referer": "http://gym.dazuiwl.cn/h5/",
    }

    res = requests.post(url, headers=headers, data=payload).json()

    try:
        if res["code"] == 1:
            if print_info:
                print("[bold green]msg: " + "可预定")
                print("[bold italic cyan]Total_Price: " + str(res["data"]["total_amount"]))
            return 1
        elif res["code"] == 0:
            if print_info:
                print("[bold red]msg: " + res["msg"])
            return 0
        elif res["code"] == 404:
            if print_info:
                print("[bold red]msg: " + res["msg"])
            return 404
        else:
            if print_info:
                print("[bold red]msg: " + "特殊情况")
            return 499
    except:
        if print_info:
            print("requests filed")
        return 123


if __name__ == "__main__":
    print(check_court_status(day="2022-05-22", court="4", book_time_1="10", book_time_2="11"))
