# GYM

For BITer book badminton

# API

1. `get_info.check_court_status()`: Get badminton court status by date, court number and begin book time(max 2).

   **Use example:**

   ```python
   check_court_status(day="2022-05-21", court="2", book_time_1="9", book_time_2="10")
   ```

   **Return example:**

   ![](https://markdown-1309012516.cos.ap-beijing.myqcloud.com/2022_5_20_17_48_37_1653040117824.png)

2. `get_status.check_bm_status()`: Get badminton all courts status by date.

   **Use example:**

   ```python
   check_bm_status(day="2022-05-21")
   ```

   **Return example:**

   ![](https://markdown-1309012516.cos.ap-beijing.myqcloud.com/2022_5_20_17_57_22_1653040642074.png)

   ![](https://markdown-1309012516.cos.ap-beijing.myqcloud.com/2022_5_20_17_58_27_1653040706993.png)

3. `submit.submit()`: use python asyncio to POST for booking court.

   **still have bug in windows**

   **need cookies & token**
