from DocXTools.choices import car_classes
from DocXTools.models import CarClass


def init_car_classes():
    CarClass.objects.all().delete()
    for c_class in car_classes:
        cl = CarClass(class_name=c_class)
        cl.save()