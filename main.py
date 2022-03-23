import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment

class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        print(week_stats)
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \ # По правилам "Бэкслеши для переносов не применяются."
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!') # Здесь круглые скобки не нужны


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        #п.1 Если здесь не делаете проверку на поддерживаемое программой указание валюты,
        # тогда в п.2 необходимо сообщить об этом пользователю
        cash_remained = self.limit - self.get_today_stats()
        """
        # Написанный ниже текст можно упростить если использовать созданные заранее словари.
        # Это позволит при небольшом добавить большое количество поддерживыаемых валют без изменения рабочего кода
        # , например:
        rates = {
        'rub' : 'руб',
        'usd' : 'USD',
        'eur' : 'Euro'
        }
        today_rate = {
        'rub' : 1.0,
        'usd' : 60,
        'eur' : 70
        }
        # Тогда проверка поддержку выбранной валюты можно проверить так:
        if currency in rates:
            cash_remained /= today_rate[currency]
            currency_type = rates[currency]
        else:
            print('Валюта пересчёта не поддерживается')
        """
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        
        # Если в п.1 не делаете проверку поддержки выбранного варианта валюты,
        # то нужно указать пользователю, что программа не поддерживает выбранное название валютной единицы
        # и предложить ему указать ту валютную единицу, которую программа поддерживает.
        
        if cash_remained > 0:
            return ( # здесь круглая скобка не нужна
                f'На сегодня осталось {round(cash_remained, 2)} ' # По правилам оформления " в f-строках не должно быть логических или арифметических операций, вызовов функций и подобной динамики"
                f'{currency_type}'
            ) # и здесь круглая скобка необязательна
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \ # По правилам "Бэкслеши для переносов не применяются."
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
        
    # Написанная ниже функция лишняя и при её вызове не возвращается ничего,
    # а именно отсутствует return:
    def get_week_stats(self):
        super().get_week_stats()

