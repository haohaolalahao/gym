# 导入requests模块
from io import BufferedRandom
from tabnanny import check

import pendulum
import requests
from rich import print
from rich.columns import Columns
from rich.console import Console
from rich.table import Table

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

def check_bm_status(require_data='tomorrow'):
    
    if require_data == 'today':
        require_data = pendulum.today().to_date_string()
    elif require_data == 'tomorrow':
        require_data = pendulum.tomorrow().to_date_string()
    else:
        pass
    
    # 请求url
    # url_bm_check_single_status = "http://gym.dazuiwl.cn/api/sport_schedule/check/id/34"
    url_bm_check_all_status_prefix = "http://gym.dazuiwl.cn/api/sport_schedule/booked/id/34?day="
    url_bm_check_price_prefix = "http://gym.dazuiwl.cn/api/sport_events/price/id/34?week=2&day="

    url_bm_check_all_status = url_bm_check_all_status_prefix + require_data
    url_bm_check_price = url_bm_check_price_prefix + require_data
    # payload = {
    #     "scene": '[{"day":"2022-05-03","fields":{"166":[328107]}}]',
    # }

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50",
        "token": "0ab1d598-6d23-4d9c-a8fd-9b9aaee62b68",
        "Host": "gym.dazuiwl.cn",
        "Origin": "http://gym.dazuiwl.cn",
        "Referer": "http://gym.dazuiwl.cn/h5/",
    }

    bm_status_res = requests.get(url_bm_check_all_status, headers=headers).json()
    bm_price_res = requests.get(url_bm_check_price, headers=headers).json()
    try:
        if bm_status_res['code'] == 1:
            bm_status_data = bm_status_res['data']
            courts = [
                '155', '156', '157', '158', '159', '160', '161', '162', '163',
                '164', '165', '166'
            ]
            times = [
                '328101', '328102', '328103', '328104', '328105', '328106',
                '328107', '328125', '328126', '328127', '328128', '328129',
                '328130', '328131', '328132'
            ]
            rows = {}
            for i in range(len(times)):
                rows[i] = []
                rows[i].append('[bold]' + str(i + 7) + ':00-' + str(i + 8) + ':00')
            i = 0
            for time in times:
                for court in courts:
                    status_key = court + '-' + time
                    if bm_status_data[status_key] == 0:
                        rows[i].append(
                            '[bold italic green]True[/bold italic green]')
                    elif bm_status_data[status_key] == 1004:
                        rows[i].append('[bold italic red]False[/bold italic red]')
                    elif bm_status_data[status_key] == 1003:
                        # 安排
                        rows[i].append(':loudly_crying_face:')
                    elif bm_status_data[status_key] == 1002:
                        # 包场
                        rows[i].append(':loudly_crying_face:')
                    elif bm_status_data[status_key] == 1001:
                        # 上课
                        rows[i].append(':loudly_crying_face:')
                i += 1
            table = Table(title=require_data + " Badminton Court",
                          header_style="bold blue")
            table.add_column("Time", style="cyan", no_wrap=True)
            table.add_column("One", justify='center', style="blue")
            table.add_column("Two", justify='center', style="blue")
            table.add_column("Three", justify='center', style="blue")
            table.add_column("Four", justify='center', style="blue")
            table.add_column("Five", justify='center', style="blue")
            table.add_column("Six", justify='center', style="blue")
            table.add_column("Seven", justify='center', style="blue")
            table.add_column("Eight", justify='center', style="blue")
            table.add_column("Nine", justify='center', style="blue")
            table.add_column("Ten", justify='center', style="blue")
            table.add_column("Eleven", justify='center', style="blue")
            table.add_column("Twelve", justify='center', style="blue")

            for i in range(len(times)):
                table.add_row(*rows[i])
            console = Console()
            console.print(table)

            # submit

        else:
            print('require filed')
    except:
        print('require filed')


    try:
        if bm_price_res['code'] == 1:
            bm_price_data = bm_price_res['data']
            m_price = bm_price_data['morning']['price']
            a_price = bm_price_data['day']['price']
            n_price = bm_price_data['night']['price']
            
            table = Table(title=require_data + " Price",
                          header_style="bold blue")
            
            table.add_column("Time", style="cyan", no_wrap=True)
            table.add_column("Price", justify='center', style="blue")

            table.add_row("Morning", str(m_price))
            table.add_row("Afternoon", str(a_price))
            table.add_row("Night", str(n_price))
        
            console = Console()
            console.print(table)

            # submit

        else:
            print('require filed')
    except:
        print('require filed')


if __name__ == "__main__":
    check_bm_status(require_data='2022-05-08')
