from datetime import datetime

from django import forms

from DocXTools.choices import citizenship_types
from DocXTools.models import Car, CarClass, Branch
from DocXTools.templates.formats import iso8601_date
from RentalService.settings_base import LENGTH_MEDIUM, LENGTH_LONG, LENGTH_SHORT


class ContractForm(forms.Form):
    contract_date = forms.DateField(label='Дата')
    contract_booking_number = forms.CharField(max_length=LENGTH_MEDIUM, label='№ бронирования')
    car = forms.ModelChoiceField(
        queryset=Car.objects.all(),
        empty_label=None,
        label='Транспортное средство'
    )
    booked_class = forms.ModelChoiceField(
        queryset=CarClass.objects.all(),
        empty_label=None,
        label='Забронирован как'
    )
    delivery_address = forms.CharField(max_length=LENGTH_LONG, label='Адрес выдачи')
    area_of_operation = forms.CharField(max_length=LENGTH_LONG, label='Территория эксплутации')
    return_address = forms.CharField(max_length=LENGTH_LONG, label='Адрес возврата')
    rent_start_date = forms.DateField(label='Начало аренды')
    rent_end_date = forms.DateField(label='Конец аренды')
    rent_start_time = forms.TimeField(label='время')
    rent_end_time = forms.TimeField(label='время')
    tenant_last_name = forms.CharField(max_length=LENGTH_MEDIUM, label='Фамилия')
    tenant_first_name = forms.CharField(max_length=LENGTH_MEDIUM, label='Имя')
    tenant_middle_name = forms.CharField(max_length=LENGTH_MEDIUM, label='Отчество')
    flight_no = forms.CharField(max_length=LENGTH_MEDIUM, label='№ рейса')
    arrive_time = forms.TimeField(label='Время прибытия')
    tenant_passport_part = forms.CharField(max_length=LENGTH_SHORT, label='Серия')
    tenant_passport_number = forms.CharField(max_length=LENGTH_MEDIUM, label='Номер')
    tenant_passport_issued = forms.CharField(max_length=LENGTH_LONG, label='Выдан')
    tenant_phone_no_contact = forms.CharField(max_length=LENGTH_MEDIUM, label='Контактный телефон')
    tenant_phone_no_working = forms.CharField(max_length=LENGTH_MEDIUM, label='Рабочий телефон')
    email = forms.EmailField(label='Электронная почта')
    tenant_driver_license_no = forms.CharField(max_length=LENGTH_MEDIUM, label='Номер')
    tenant_driver_license_issued = forms.CharField(max_length=LENGTH_LONG, label='Выдано')

    citizenship = forms.CharField(max_length=LENGTH_LONG, label='Гражданство')
    birth_date = forms.DateField(label='Дата рождения')
    tenant_registration_address = forms.CharField(max_length=LENGTH_LONG, label='Адрес регистрации')
    tenant_residential_address = forms.CharField(max_length=LENGTH_LONG, label='Адрес проживания')

    driver2_first_name = forms.CharField(max_length=LENGTH_MEDIUM, label='Имя', required=False)
    driver2_middle_name = forms.CharField(max_length=LENGTH_MEDIUM, label='Отчество', required=False)
    driver2_last_name = forms.CharField(max_length=LENGTH_MEDIUM, label='Фамилия', required=False)
    driver2_passport_part = forms.CharField(max_length=LENGTH_SHORT, label='Серия', required=False)
    driver2_passport_number = forms.CharField(max_length=LENGTH_MEDIUM, label='Номер', required=False)
    driver2_passport_issued = forms.CharField(max_length=LENGTH_LONG, label='Выдан', required=False)
    driver2_driver_license_no = forms.CharField(max_length=LENGTH_MEDIUM, label='Номер', required=False)
    driver2_driver_license_issued = forms.CharField(max_length=LENGTH_LONG, label='Выдано', required=False)
    driver2_registration_address = forms.CharField(max_length=LENGTH_LONG, label='Адрес регистрации', required=False)
    driver2_phone_no_contact = forms.CharField(max_length=LENGTH_MEDIUM, label='Контактный телефон', required=False)

    driver3_first_name = forms.CharField(max_length=LENGTH_MEDIUM, label='Имя', required=False)
    driver3_middle_name = forms.CharField(max_length=LENGTH_MEDIUM, label='Отчество', required=False)
    driver3_last_name = forms.CharField(max_length=LENGTH_MEDIUM, label='Фамилия', required=False)
    driver3_passport_part = forms.CharField(max_length=LENGTH_SHORT, label='Серия', required=False)
    driver3_passport_number = forms.CharField(max_length=LENGTH_MEDIUM, label='Номер', required=False)
    driver3_passport_issued = forms.CharField(max_length=LENGTH_LONG, label='Выдан', required=False)
    driver3_driver_license_no = forms.CharField(max_length=LENGTH_MEDIUM, label='Номер', required=False)
    driver3_driver_license_issued = forms.CharField(max_length=LENGTH_LONG, label='Выдано', required=False)
    driver3_registration_address = forms.CharField(max_length=LENGTH_LONG, label='Адрес регистрации', required=False)
    driver3_phone_no_contact = forms.CharField(max_length=LENGTH_MEDIUM, label='Контактный телефон', required=False)

    car_current_volume = forms.IntegerField(label='Текущая ёмкость')
    
    
class CalcForm(forms.Form):
    booking_date = forms.DateField(label='Дата бронирования', initial=datetime.now().date().strftime(iso8601_date))
    car_class = forms.ModelChoiceField(
        queryset=CarClass.objects.all(),
        empty_label=None,
        label='Класс автомобиля'
    )
    days = forms.IntegerField()
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        empty_label=None,
        label='Подразделение'
    )
    citizenship = forms.ChoiceField(
        choices=citizenship_types,
        label='Гражданство'
    )
