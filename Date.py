from typing import Any, Union


class Date:
    DAY_OF_MONTH = ((31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31),  #
                    (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31))  #

    def __init__(self, year, month, day):
        if not Date.__is_valid_date(year, month, day):
            raise ValueError
        self._year = year
        self._month = month
        self._day = day

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value):
        if Date.__is_valid_date(self.year, self.month, value):
            self._day = value

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value):
        if Date.__is_valid_date(self.year, value, self.day):
            self._month = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if Date.__is_valid_date(value, self.month, self.day):
            self._year = value

    def __str__(self):
        return f"{self._day} - {self._month} - {self._year}"

    def __repr__(self):
        return f'{self.day} {self.month} {self.year}'

    @staticmethod
    def is_leap_year(year):
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            return True
        else:
            return False

    @classmethod
    def get_max_day(cls, year, month):
        return cls.DAY_OF_MONTH[cls.is_leap_year(year)][month - 1]

    @property
    def date(self):
        return f"{self.year}.{self.month}.{self.date}"

    @date.setter
    def date(self, value: str):  # 2020.12.6
        list_of_numb = value.split(".")
        if len(list_of_numb) != 3:
            raise ValueError
        year = int(list_of_numb[0])
        month = int(list_of_numb[1])
        day = int(list_of_numb[2])
        self.__is_valid_date(year, month, day)
        self._day = day
        self._year = year
        self._month = month

    @classmethod
    def __is_valid_date(cls, year, month, day):
        if not isinstance(year, int):
            raise TypeError
        if not isinstance(month, int):
            raise TypeError
        if not isinstance(day, int):
            raise TypeError
        if year <= 0 or month <= 0 or day <= 0:
            raise ValueError
        if day <= cls.get_max_day(year, month) and month <= 12:
            return True
        else:
            raise ValueError

    def add_day(self, day):
        if not isinstance(day, int) or day < 0:
            raise TypeError
        current_add = self._day + day
        if current_add > Date.get_max_day(self._year, self._month):
            while current_add > Date.get_max_day(self._year, self._month):
                current_add = current_add - Date.get_max_day(self._year, self._month)
                self.add_month(1)
        self._day = current_add

    def add_month(self, add_m):
        if not isinstance(add_m, int) or add_m < 0:
            raise TypeError
        if add_m >= 12:
            add_year1 = add_m // 12
            add_month1 = add_m % 12
        else:
            add_year1 = 0
            add_month1 = add_m

        if self._month + add_month1 > 12:
            add_year2 = 1
            add_month2 = self._month + add_month1 - 12
        else:
            add_year2 = 0
            add_month2 = self._month + add_month1

        self._year = self._year + add_year1 + add_year2
        self._month = add_month2

        if self._day > Date.get_max_day(self._year, self._month):
            self._day = Date.get_max_day(self._year, self._month)

    def add_year(self, add_y):
        if not isinstance(add_y, int) or add_y < 0:
            raise TypeError
        self._year = self._year + add_y

        if self._day > Date.get_max_day(self._year, self._month):
            self._day = Date.get_max_day(self._year, self._month)

    @staticmethod
    def date2_date1(date2, date1):
        list_of_numb2 = date2.split(".")
        if len(list_of_numb2) != 3:
            raise ValueError
        year2 = int(list_of_numb2[0])
        month2 = int(list_of_numb2[1])
        day2 = int(list_of_numb2[2])
        Date.__is_valid_date(year2, month2, day2)

        list_of_numb1 = date1.split(".")
        if len(list_of_numb1) != 3:
            raise ValueError
        year1 = int(list_of_numb1[0])
        month1 = int(list_of_numb1[1])
        day1 = int(list_of_numb1[2])
        Date.__is_valid_date(year1, month1, day1)

        days_date2 = day2
        for i in range(1, year2):
            for k in range(1, 13):
                days_date2 += Date.get_max_day(i, k)
        for i in range(1, month2):
            days_date2 += Date.get_max_day(year2, i)

        days_date1 = day1
        for i in range(1, year1):
            for k in range(1, 13):
                days_date1 += Date.get_max_day(i, k)
        for i in range(1, month1):
            days_date1 += Date.get_max_day(year1, i)

        if days_date2 < days_date1:
            raise ValueError("Неправильны введены данные, первая дата должна быть больше")

        return days_date2 - days_date1





if __name__ == '__main__':
    # some_date = Date()
    # some_date.date = "2020.7.1"
    # check1 = Date.get_max_day(2019, 2)
    # print(some_date)
    # some_date.add_day(2)
    # print(check1)
    # print(some_date)

    # d1 = Date(2020, 7, 11)
    # d2 = Date(2020, 2, 28)
    print(Date.date2_date1("2035.12.11", "2017.12.11"))
    #Date.date2_date1(d1, d2)  -> days = ?
