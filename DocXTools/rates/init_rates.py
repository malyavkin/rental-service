from DocXTools.models import *
from DocXTools.templates.formats import iso8601_date
from DocXTools.choices import car_classes
day_intervals = [
    (1, 2),
    (3, 6),
    (7, 7),
    (8, 14),
    (15, 30)
]

car_classes = [CarClass.objects.get(class_name=i) for i in car_classes]

rent_configs = [
    {
        'booking_interval': (
            datetime.strptime('2016-07-01', iso8601_date).date(),
            datetime.strptime('2016-09-25', iso8601_date).date()
        ),
        'branch_name': 'Симферополь',
        'currency': 'USD',
        'citizenship': 'rus',
        'prices': [
            [39.00, 36.00, 180.00, 33.00, 32.00],
            [45.00, 42.00, 210.00, 39.00, 38.00],
            [70.00, 64.00, 320.00, 59.00, 58.00],
            [88.00, 80.00, 400.00, 73.00, 72.00],
            [40.00, 37.00, 185.00, 34.00, 33.00],
            [61.00, 57.00, 285.00, 54.00, 53.00],
            [97.00, 88.00, 440.00, 80.00, 79.00],
            [69.00, 63.00, 315.00, 58.00, 57.00],
            [50.50, 47.00, 235.00, 44.00, 43.00],
            [55.00, 52.00, 260.00, 48.00, 45.00],
        ]

    },
    {
        'booking_interval': (
            datetime.strptime('2016-09-25', iso8601_date).date(),
            datetime.strptime('2016-12-30', iso8601_date).date()
        ),
        'branch_name': 'Симферополь',
        'currency': 'USD',
        'citizenship': 'rus',
        'prices': [
            [33.2, 30.6, 153.0, 28.1, 27.2],
            [38.3, 35.7, 178.5, 33.2, 32.3],
            [59.5, 54.4, 272.0, 50.2, 49.3],
            [74.8, 68.0, 340.0, 62.1, 61.2],
            [34.0, 31.5, 157.3, 28.9, 28.1],
            [51.9, 48.5, 242.3, 45.9, 45.1],
            [82.5, 74.8, 374.0, 68.0, 67.2],
            [58.7, 53.6, 267.8, 49.3, 48.5],
            [42.9, 40.0, 199.8, 37.4, 36.6],
            [46.8, 44.2, 221.0, 40.8, 38.3],
        ]

    },
    {
        'booking_interval': (
            datetime.strptime('2016-12-30', iso8601_date).date(),
            datetime.strptime('2017-05-30', iso8601_date).date()
        ),
        'branch_name': 'Симферополь',
        'currency': 'USD',
        'citizenship': 'rus',
        'prices': [
            [29.8, 27.5, 137.7, 25.2, 24.5],
            [34.4, 32.1, 160.7, 29.8, 29.1],
            [53.6, 49.0, 244.8, 45.1, 44.4],
            [67.3, 61.2, 306.0, 55.8, 55.1],
            [30.6, 28.3, 141.5, 26.0, 25.2],
            [46.7, 43.6, 218.0, 41.3, 40.5],
            [74.2, 67.3, 336.6, 61.2, 60.4],
            [52.8, 48.2, 241.0, 44.4, 43.6],
            [38.6, 36.0, 179.8, 33.7, 32.9],
            [42.1, 39.8, 198.9, 36.7, 34.4],
        ]

    },
    {
        'booking_interval': (
            datetime.strptime('2017-05-30', iso8601_date).date(),
            datetime.strptime('2017-09-24', iso8601_date).date()
        ),
        'branch_name': 'Симферополь',
        'currency': 'USD',
        'citizenship': 'rus',
        'prices': [
            [37.1, 34.2, 171.0, 31.4, 30.4],
            [42.8, 39.9, 199.5, 37.1, 36.1],
            [66.5, 60.8, 304.0, 56.1, 55.1],
            [83.6, 76.0, 380.0, 69.4, 68.4],
            [38.0, 35.2, 175.8, 32.3, 31.4],
            [58.0, 54.2, 270.8, 51.3, 50.4],
            [92.2, 83.6, 418.0, 76.0, 75.1],
            [65.6, 59.9, 299.3, 55.1, 54.2],
            [48.0, 44.7, 223.3, 41.8, 40.9],
            [52.3, 49.4, 247.0, 45.6, 42.8],
        ]

    },
    {  # second line

        'booking_interval': (
            datetime.strptime('2016-07-01', iso8601_date).date(),
            datetime.strptime('2016-09-25', iso8601_date).date()
        ),
        'branch_name': 'Симферополь',
        'currency': 'USD',
        'citizenship': '*',
        'prices': [
            [ 45.00,  41.00, 207.00, 38.00, 37.0],
            [ 52.00,  48.00, 242.00, 45.00, 44.0],
            [ 81.00,  74.00, 368.00, 68.00, 67.0],
            [ 101.00, 92.00, 460.00, 84.00, 83.0],
            [ 46.00,  43.00, 213.00, 39.00, 38.0],
            [ 70.00,  66.00, 328.00, 62.00, 61.0],
            [112.00, 101.00, 506.00, 92.00, 91.0],
            [ 79.00,  72.00, 362.00, 67.00, 66.0],
            [ 58.00,  54.00, 270.00, 51.00, 49.0],
            [ 63.00,  60.00, 299.00, 55.00, 52.0],
        ]

    },
    {
        'booking_interval': (
            datetime.strptime('2016-09-25', iso8601_date).date(),
            datetime.strptime('2016-12-30', iso8601_date).date()
        ),
        'branch_name': 'Симферополь',
        'currency': 'USD',
        'citizenship': '*',
        'prices': [
            [34.8, 32.1, 160.7, 29.5, 28.6],
            [40.2, 37.5, 187.4, 34.8, 33.9],
            [62.5, 57.1, 285.6, 52.7, 51.8],
            [78.5, 71.4, 357.0, 65.2, 64.3],
            [35.7, 33.0, 165.1, 30.3, 29.5],
            [54.4, 50.9, 254.4, 48.2, 47.3],
            [86.6, 78.5, 392.7, 71.4, 70.5],
            [61.6, 56.2, 281.1, 51.8, 50.9],
            [45.1, 41.9, 209.7, 39.3, 38.4],
            [49.1, 46.4, 232.1, 42.8, 40.2],
        ]

    },
    {
        'booking_interval': (
            datetime.strptime('2016-12-30', iso8601_date).date(),
            datetime.strptime('2017-05-30', iso8601_date).date()
        ),
        'branch_name': 'Симферополь',
        'currency': 'USD',
        'citizenship': '*',
        'prices': [
            [31.3, 28.9, 144.6, 26.5, 25.7],
            [36.1, 33.7, 168.7, 31.3, 30.5],
            [56.2, 51.4, 257.0, 47.4, 46.6],
            [70.7, 64.3, 321.3, 58.6, 57.8],
            [32.1, 29.7, 148.6, 27.3, 26.5],
            [49.0, 45.8, 228.9, 43.4, 42.6],
            [77.9, 70.7, 353.4, 64.3, 63.5],
            [55.4, 50.6, 253.0, 46.6, 45.8],
            [40.6, 37.8, 188.8, 35.3, 34.5],
            [44.2, 41.8, 208.8, 38.6, 36.1],
        ]

    },
    {
        'booking_interval': (
            datetime.strptime('2017-05-30', iso8601_date).date(),
            datetime.strptime('2017-09-24', iso8601_date).date()
        ),
        'branch_name': 'Симферополь',
        'currency': 'USD',
        'citizenship': '*',
        'prices': [
            [38.9, 35.9, 179.6, 32.9, 31.9],
            [44.9, 41.9, 209.5, 38.9, 37.9],
            [69.8, 63.8, 319.2, 58.9, 57.9],
            [87.8, 79.8, 399.0, 72.8, 71.8],
            [39.9, 36.9, 184.5, 33.9, 32.9],
            [60.8, 56.9, 284.3, 53.9, 52.9],
            [96.8, 87.8, 438.9, 79.8, 78.8],
            [68.8, 62.8, 314.2, 57.9, 56.9],
            [50.4, 46.9, 234.4, 43.9, 42.9],
            [54.9, 51.9, 259.4, 47.9, 44.9],
        ]

    },
    {
        'booking_interval': (
            datetime.strptime('2016-12-10', iso8601_date).date(),
            datetime.strptime('2017-03-15', iso8601_date).date()
        ),
        'branch_name': 'Сочи',
        'currency': 'USD',
        'citizenship': 'rus',
        'prices': [
            [30.0, 29.0, 152.0, 21.0, 20.0],
            [33.0, 30.0, 163.0, 21.0, 21.0],
            [50.0, 43.0, 252.0, 30.0, 29.0],
            [55.0, 48.0, 273.0, 34.0, 34.0],
            [35.0, 31.0, 174.0, 22.0, 21.0],
            [40.0, 35.0, 199.0, 29.0, 28.0],
            [75.0, 61.0, 373.0, 47.0, 46.0],
            [79.0, 70.0, 397.0, 57.0, 51.0],
            [36.0, 32.0, 179.0, 23.0, 22.0],
            [84.0, 74.0, 422.0, 62.0, 53.0],
        ]

    },
    {
        'booking_interval': (
            datetime.strptime('2016-12-10', iso8601_date).date(),
            datetime.strptime('2017-03-15', iso8601_date).date()
        ),
        'branch_name': 'Сочи',
        'currency': 'USD',
        'citizenship': '*',
        'prices': [
            [30.0, 29.0, 152.0, 21.0, 20.0],
            [33.0, 30.0, 163.0, 21.0, 21.0],
            [50.0, 43.0, 252.0, 30.0, 29.0],
            [55.0, 48.0, 273.0, 34.0, 34.0],
            [35.0, 31.0, 174.0, 22.0, 21.0],
            [40.0, 35.0, 199.0, 29.0, 28.0],
            [75.0, 61.0, 373.0, 47.0, 46.0],
            [79.0, 70.0, 397.0, 57.0, 51.0],
            [36.0, 32.0, 179.0, 23.0, 22.0],
            [84.0, 74.0, 422.0, 62.0, 53.0],
        ]

    },

]


def create_rate(car_class, day_interval, booking_interval, branch_name, currency, citizenship, price):
    rate = Rate()
    rate.branch = Branch.objects.get(name=branch_name)
    rate.booking_from = booking_interval[0]
    rate.booking_to = booking_interval[1]
    rate.citizenship = citizenship
    rate.days_from = day_interval[0]
    rate.days_to = day_interval[1]
    rate.car_class = car_class
    rate.price = price
    rate.currency = currency
    rate.rent_type = 'd' if day_interval[0] != day_interval[1] else 'r'
    rate.save()
    o = rate.get_json()
    print(json.dumps(o, ensure_ascii=False, indent=4, sort_keys=True))


def init_rates():
    Rate.objects.all().delete()

    for config in rent_configs:
        for i in range(len(config['prices'])):
            for j in range(len(config['prices'][i])):
                create_rate(car_class=car_classes[i],
                            day_interval=day_intervals[j],
                            booking_interval=config['booking_interval'],
                            branch_name=config['branch_name'],
                            currency=config['currency'],
                            citizenship=config['citizenship'],
                            price=config['prices'][i][j])
