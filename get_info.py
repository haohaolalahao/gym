# 导入requests模块
import pendulum
import requests
from rich import print

# pingpang 33 badminton 34
# badminton
# 场次
# 1   2   3   4   5   6   7   8   9   10  11  12
# 155 156 157 158 159 160 161 162 163 164 165 166
# time 7-8    8-9    9-10   10-11  11-12  12-13  13-14
# time 328101 328102 328103 328104 328105 328106 328107
# time max 2
# 后面时段不可定

# pingpang
# 1   2   3   4   5   6   7   8   9   10
# 145 146 147 148 149 150 151 152 153 154
# time 7-8    8-9    9-10   10-11  11-12  12-13  13-14
# time 328094 328095 328096 328097 328098 328099 328100
# time max 2


# 请求url
def check_court_status(day: str = "tomorrow",
                       court: str = '1',
                       book_time_1: str = '7',
                       book_time_2: str = '',
                       print_info: bool = True):
    if day == "today":
        day = pendulum.today().to_date_string()
    elif day == "tomorrow":
        day = pendulum.tomorrow().to_date_string()
    else:
        pass

    courts = [
        '155', '156', '157', '158', '159', '160', '161', '162', '163', '164',
        '165', '166'
    ]
    court_times = [
        '328101', '328102', '328103', '328104', '328105', '328106', '328107',
        '328125', '328126', '328127', '328128', '328129', '328130', '328131',
        '328132'
    ]

    court_index = int(eval(court))
    assert 1 <= court_index <= 12, 'bad court number'
    book_time_index_1 = int(eval(book_time_1))
    assert 7 <= book_time_index_1 <= 21, 'bad book time first'

    if book_time_2 == '':
        book_time_index_2 = False
    else:
        book_time_index_2 = int(eval(book_time_2))
        assert 7 <= book_time_index_2 <= 21, 'bad book time second'

    court = courts[court_index - 1]
    if book_time_index_2:
        book_time = court_times[book_time_index_1 -
                                7] + ', ' + court_times[book_time_index_2 - 7]
    else:
        book_time = court_times[book_time_index_1 - 7]

    if print_info:
        print('[bold blue]Check time: ', day)
        print('[bold blue]Check court: ', str(court_index))
        if book_time_index_2:
            print('[bold blue]Check book time: ',
                  str(book_time_index_1) + ', ' + str(book_time_index_2))
        else:
            print('[bold blue]Check book time: ', str(book_time_index_1))

    scene = '[{"day":"' + f'{day}' + '","fields":{"' + f'{court}' + '":[' + f'{book_time}' + ']}}]'

    # print(scene)
    url = "http://gym.dazuiwl.cn/api/sport_schedule/check/id/34"

    # 请求参数
    payload = {
        "scene": scene,
    }

    # head
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50",
        "token": "0ab1d598-6d23-4d9c-a8fd-9b9aaee62b68",
        "Host": "gym.dazuiwl.cn",
        "Origin": "http://gym.dazuiwl.cn",
        "Referer": "http://gym.dazuiwl.cn/h5/",
    }
    # cookies
    # cookie = {"PHPSESSID": "392enpsjdnre0svp25m8e31cmm"}
    # form表单形式，参数用data
    res = requests.post(url, headers=headers, data=payload).json()

    try:
        if res['code'] == 1:
            if print_info:
                print('[bold green]msg: ' + '可预定')
                print('[bold italic cyan]Total_Price: ' + str(res['data']['total_amount']))
            return 1
        elif res['code'] == 0:
            if print_info:
                print('[bold red]msg: ' + res['msg'])
            return 0
        elif res['code'] == 404:
            if print_info:
                print('[bold red]msg: ' + res['msg'])
            return 404
        else:
            if print_info:
                print('[bold red]msg: ' + '特殊情况')
            return 499
    except:
        if print_info:
            print('requests filed')
        return 123


if __name__ == "__main__":
    print(
        check_court_status(day='2022-05-08',
                           court='1',
                           book_time_1='9',
                           book_time_2='10'))
