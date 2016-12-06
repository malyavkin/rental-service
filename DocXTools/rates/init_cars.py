import csv
from datetime import datetime
from DocXTools.models import Car, CarClass, Company

filename = 'DocXTools/rates/park.csv'

SKIP_FIRST_LINE = True


def init_cars():
    saved = 0
    with open(filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        Car.objects.all().delete()
        line_no = 0
        for row in csv_reader:
            line_no += 1
            if line_no == 1 and SKIP_FIRST_LINE:
                continue

            try:
                car = Car()
                car.car_class = CarClass.objects.get(class_name=row[0])
                car.license_no = row[1]
                car.vendor = row[2]
                car.model = row[3]
                car.model_type = row[4]
                car.color = row[5]
                car.transmission = 'm' if row[6] == 'РКП' else 'a'
                car.power = int(row[7])
                car.VIN = row[8]
                car.STS = row[9]
                car.year = int(row[10])
                # 11
                try:
                    car.reg_date = datetime.strptime(row[11], '%m/%d/%Y')
                except Exception as x:
                    print(x)

                # 12
                car.owner = Company.objects.get(org_prefix=row[12])
                # 13
                car.PTS = row[13]
                # 14
                car.service_book = True if row[14] else False
                # 15
                car.OSAGO = row[15]
                # 16
                try:
                   car.OSAGO_until = datetime.strptime(row[16], '%m/%d/%Y')
                except Exception as x:
                    print(x)


                # 17
                try:
                    car.OSAGO_premium = float(row[17])
                except Exception as x:
                   print(x)

                # 18
                car.KASKO = row[18]
                # 19
                try:
                    car.KASKO_until = datetime.strptime(row[19], '%m/%d/%Y')
                except Exception as x:
                    print(x)

                # 20
                try:
                    car.KASKO_insurance = int(row[20])
                except Exception as x:
                    print(x)

                # 21
                try:
                    car.KASKO_premium = float(row[21])
                except Exception as x:
                    print(x)

                # 22
                try:
                   car.KASKO_percent = float(row[22].replace("%", ""))
                except Exception as x:
                   print(x)
                # 23
                car.damages = row[23] if row[23] != 'NONE' else ''
                car.save()
                saved += 1
            except Exception as x:
                print("general", x)

    print(saved)
