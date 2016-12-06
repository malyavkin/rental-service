import json

from datetime import date, datetime
from django.contrib.auth.models import User
from django.db import models

from RentalService.settings_base import LENGTH_MEDIUM, LENGTH_LONG, LENGTH_SHORT
from .choices import *


# todo: circular deps
class SerializableMixin:
    def get_json(self):
        o = {}
        fields = self._meta.get_fields()
        for field in fields:
            if isinstance(field, models.ManyToOneRel):
                pass
            elif isinstance(field, models.ForeignKey):
                foreign = getattr(self, field.name)
                if isinstance(foreign, SerializableMixin):
                    o[field.name] = foreign.get_json()
                elif isinstance(foreign, User):
                    o[field.name] = {
                        'first_name': foreign.first_name,
                        'last_name': foreign.last_name,
                        'username': foreign.username
                    }
                else:
                    print('Warning! Field {} cannot be serialized!'.format(field.name))
                    o[field.name] = foreign.__str__()
            else:
                value = getattr(self, field.name)
                if isinstance(value, (date, datetime)):
                    o[field.name] = getattr(self, field.name).isoformat()
                else:
                    o[field.name] = getattr(self, field.name)
        return o


class Company(models.Model, SerializableMixin):
    org_name = models.CharField(max_length=LENGTH_LONG, verbose_name='Организация')
    org_prefix = models.CharField(max_length=LENGTH_LONG, verbose_name='Префикс')

    def __str__(self):
        return self.org_name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Representative(models.Model, SerializableMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_authority_id = models.CharField(max_length=LENGTH_LONG, verbose_name='Номер доверенности')
    issue_date = models.DateField(verbose_name='Дата выдачи доверенности')
    middle_name = models.CharField(max_length=LENGTH_LONG, verbose_name='Отчество')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)

    def get_initials(self):
        return '{} {}. {}.'.format(self.user.last_name, self.user.first_name[:1], self.middle_name[:1])

    def __str__(self):
        return self.get_initials()

    class Meta:
        verbose_name = 'Ответственное лицо'
        verbose_name_plural = 'Ответственные лица'


class CarClass(models.Model, SerializableMixin):
    class_name = models.CharField(max_length=5, verbose_name='Класс')

    def __str__(self):
        return self.class_name

    class Meta:
        verbose_name = 'Класс автомобиля'
        verbose_name_plural = 'Классы автомобиля'


class Car(models.Model, SerializableMixin):

    car_class = models.ForeignKey(to=CarClass, on_delete=models.SET_NULL, null=True)
    license_no = models.CharField(max_length=LENGTH_SHORT, verbose_name='Гос. номер')
    vendor = models.CharField(max_length=LENGTH_LONG, verbose_name='Марка')
    model = models.CharField(max_length=LENGTH_LONG, verbose_name='Модель')
    model_type = models.CharField(max_length=LENGTH_LONG, verbose_name='Кузов')
    color = models.CharField(max_length=LENGTH_LONG, verbose_name='Цвет')
    transmission = models.CharField(max_length=1, verbose_name='КПП', choices=transmission_types)
    power = models.IntegerField(verbose_name='Мощность двигателя (л.с.)')
    VIN = models.CharField(max_length=LENGTH_MEDIUM)
    STS = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='СТС')
    year = models.IntegerField(verbose_name='Год выпуска')
    reg_date = models.DateField(verbose_name='Дата регистрации')
    owner = models.CharField(max_length=LENGTH_LONG, verbose_name='Собственник')
    PTS = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='ПТС')
    service_book = models.BooleanField(verbose_name='Сервисная книжка')
    OSAGO = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='ОСАГО Ресо-Гарантия', null=True, blank=True)
    OSAGO_until = models.DateField(verbose_name='ОСАГО до', null=True, blank=True)
    OSAGO_premium = models.FloatField(verbose_name='ОСАГО премия', null=True, blank=True)
    KASKO = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='КАСКО Ресо-Гарантия', null=True, blank=True)
    KASKO_until = models.DateField(verbose_name='КАСКО до', null=True, blank=True)
    KASKO_insurance = models.FloatField(verbose_name='КАСКО страховая сумма', null=True, blank=True)
    KASKO_premium = models.FloatField(verbose_name='КАСКО премия', null=True, blank=True)
    KASKO_percent = models.FloatField(verbose_name='КАСКО %', null=True, blank=True)
    damages = models.TextField(verbose_name='Повреждения')

    def __str__(self):
        return '{} {}'.format(self.vendor, self.license_no)

    def str_with_class(self):
        return '{} {} ({})'.format(self.vendor, self.license_no, self.car_class)

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'


class Address(models.Model, SerializableMixin):
    address = models.CharField(max_length=LENGTH_LONG)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Contract(models.Model, SerializableMixin):
    number = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='№ договора аренды')
    # без сквозного, т.е. 2016_11 (для 2016_11_123)
    number_order = models.IntegerField(verbose_name='№ договора сквозной')
    # только сквозная часть, т.е. 123 (для 2016_11_123)
    contract_date = models.DateField(verbose_name='Дата')
    contract_booking_number = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='№ бронирования')

    agent = models.ForeignKey(Representative, on_delete=models.SET_NULL, null=True, verbose_name='Арендодатель')
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, verbose_name='Транспортное средство')
    booked_class = models.ForeignKey(to=CarClass, on_delete=models.SET_NULL,
                                     null=True, verbose_name='Забронированный класс')
    delivery_address = models.CharField(max_length=LENGTH_LONG, verbose_name='Адрес выдачи')
    area_of_operation = models.CharField(max_length=LENGTH_LONG, verbose_name='Территория эксплутации')
    return_address = models.CharField(max_length=LENGTH_LONG, verbose_name='Адрес возврата')
    rent_start_date = models.DateField(verbose_name='Начало срока аренды', null=True)
    rent_start_time = models.TimeField(verbose_name='Начало срока аренды', null=True)
    rent_end_date = models.DateField(verbose_name='Конец срока аренды', null=True)
    rent_end_time = models.TimeField(verbose_name='Конец срока аренды', null=True)
    # Renter data
    flight_no = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='№ рейса')
    arrive_time = models.TimeField(verbose_name='Время прилета')

    tenant_first_name = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='Имя')
    tenant_middle_name = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='Отчество')
    tenant_last_name = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='Фамилия')

    tenant_passport_part = models.CharField(max_length=LENGTH_SHORT, verbose_name='Серия паспорта')
    tenant_passport_number = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='Номер паспорта')
    tenant_passport_issued = models.CharField(max_length=LENGTH_LONG, verbose_name='Паспорт выдан')

    tenant_phone_no_contact = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='Контактный телефон')
    tenant_phone_no_working = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='Рабочий телефон')
    email = models.EmailField(verbose_name='Электронная почта')

    tenant_driver_license_no = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='№ водительского удостоверения')
    tenant_driver_license_issued = models.CharField(max_length=LENGTH_LONG,
                                                    verbose_name='Водительское удостоверение выдано')

    citizenship = models.CharField(max_length=LENGTH_LONG, verbose_name='Гражданство')
    birth_date = models.DateField(verbose_name='Дата рождения')
    tenant_registration_address = models.CharField(max_length=LENGTH_LONG, verbose_name='Адрес регистрации')
    tenant_residential_address = models.CharField(max_length=LENGTH_LONG, verbose_name='Адрес проживания')
    # second driver

    driver2_first_name = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='Имя', blank=True)
    driver2_middle_name = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='Отчество', blank=True)
    driver2_last_name = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='Фамилия', blank=True)
    driver2_passport_part = models.CharField(max_length=LENGTH_SHORT, verbose_name='Серия паспорта', blank=True)
    driver2_passport_number = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='Номер паспорта', blank=True)
    driver2_passport_issued = models.CharField(max_length=LENGTH_LONG, verbose_name='Паспорт выдан', blank=True)
    driver2_driver_license_no = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='№ водительского удостоверения',
                                                 blank=True)
    driver2_driver_license_issued = models.CharField(max_length=LENGTH_LONG,
                                                     verbose_name='Водительское удостоверение выдано',
                                                     blank=True)
    driver2_registration_address = models.CharField(max_length=LENGTH_LONG,
                                                    verbose_name='Адрес регистрации', blank=True)
    driver2_phone_no_contact = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='Контактный телефон', blank=True)
    # third driver

    driver3_first_name = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='Имя', blank=True)
    driver3_middle_name = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='Отчество', blank=True)
    driver3_last_name = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='Фамилия', blank=True)
    driver3_passport_part = models.CharField(max_length=LENGTH_SHORT, verbose_name='Серия паспорта', blank=True)
    driver3_passport_number = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='Номер паспорта', blank=True)
    driver3_passport_issued = models.CharField(max_length=LENGTH_LONG, verbose_name='Паспорт выдан', blank=True)
    driver3_driver_license_no = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='№ водительского удостоверения',
                                                 blank=True)
    driver3_driver_license_issued = models.CharField(max_length=LENGTH_LONG,
                                                     verbose_name='Водительское удостоверение выдано',
                                                     blank=True)
    driver3_registration_address = models.CharField(max_length=LENGTH_LONG,
                                                    verbose_name='Адрес регистрации', blank=True)
    driver3_phone_no_contact = models.CharField(max_length=LENGTH_MEDIUM, verbose_name='Контактный телефон', blank=True)

    car_state_when_signed = models.TextField(verbose_name='[json] car state upon signation')
    rep_state_when_signed = models.TextField(verbose_name='[json] representative state upon signation')

    car_current_volume = models.IntegerField(verbose_name='Текущая ёмкость')

    def get_complete_number(self):
        return '{}_{}_{}'.format(self.get_agent_state()['company']['org_prefix'],
                                 self.number,
                                 self.number_order)

    def get_car_state(self):
        return json.loads(self.car_state_when_signed)

    def get_agent_state(self):
        return json.loads(self.rep_state_when_signed)

    def car_class_equals_booked_class(self):
        booked_class = self.booked_class.class_name
        car_class = self.get_car_state()['car_class']['class_name']
        return booked_class == car_class

    def get_driver_license(self, driver_no):
        if driver_no == 1:
            return '№{}; выдано {}'.format(self.tenant_driver_license_no,
                                           self.tenant_driver_license_issued)
        elif driver_no == 2:
            return '№{}; выдано {}'.format(self.driver2_driver_license_no,
                                           self.driver2_driver_license_issued)
        elif driver_no == 3:
            return '№{}; выдано {}'.format(self.driver3_driver_license_no,
                                           self.driver3_driver_license_issued)

    def get_driver_fio(self, driver_no):
        if driver_no == 1:
            return '{} {} {}'.format(self.tenant_last_name,
                                     self.tenant_first_name,
                                     self.tenant_middle_name)
        elif driver_no == 2:
            return '{} {} {}'.format(self.driver2_last_name,
                                     self.driver2_first_name,
                                     self.driver2_middle_name)
        elif driver_no == 3:
            return '{} {} {}'.format(self.driver3_last_name,
                                     self.driver3_first_name,
                                     self.driver3_middle_name)

    def get_driver_passport(self, driver_no):
        if driver_no == 1:
            return '№{} {}; выдан {}'.format(self.tenant_passport_part,
                                             self.tenant_passport_number,
                                             self.tenant_passport_issued)
        elif driver_no == 2:
            return '№{} {}; выдан {}'.format(self.driver2_passport_part,
                                             self.driver2_passport_number,
                                             self.driver2_passport_issued)
        elif driver_no == 3:
            return '№{} {}; выдан {}'.format(self.driver3_passport_part,
                                             self.driver3_passport_number,
                                             self.driver3_passport_issued)

    def __str__(self):
        return '{} от {} ({})'.format(self.get_complete_number(), self.contract_date, self.car)

    def save(self, *args, **kwargs):
        if self.number_order is None:
            new_number_order = 0

            latest_contracts = Contract.objects.order_by('-number_order')
            if latest_contracts:
                latest_contract = Contract.objects.order_by('-number_order')[0]
                new_number_order = latest_contract.number_order + 1

            now = datetime.now()
            self.number = now.strftime('%Y_%m')
            self.number_order = new_number_order
            self.car_state_when_signed = json.dumps(self.car.get_json())
            self.rep_state_when_signed = json.dumps(self.agent.get_json())
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'


class DocXTemplate(models.Model, SerializableMixin):
    template_path = models.CharField(max_length=LENGTH_LONG)
    template_name = models.CharField(max_length=LENGTH_LONG)

    def __str__(self):
        return self.template_name

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'


class DocXDocument(models.Model, SerializableMixin):
    path = models.CharField(max_length=LENGTH_LONG)
    template = models.ForeignKey(to=DocXTemplate, on_delete=models.SET_NULL, null=True)
    contract = models.ForeignKey(to=Contract, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class Branch(models.Model, SerializableMixin):
    name = models.CharField(max_length=LENGTH_MEDIUM)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'


class Rate(models.Model, SerializableMixin):
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE, null=True)
    booking_from = models.DateField(null=True)
    booking_to = models.DateField(null=True)
    citizenship = models.CharField(max_length=LENGTH_SHORT, null=True, choices=citizenship_types)
    days_from = models.IntegerField(null=True)
    days_to = models.IntegerField(null=True)
    car_class = models.ForeignKey(to=CarClass, on_delete=models.CASCADE, null=True)
    price = models.FloatField()
    currency = models.CharField(max_length=3, null=True)
    rent_type = models.CharField(max_length=1, choices=rent_rate_types)

    def get_total_for_days(self, days):
        if days > self.days_to or days < self.days_from:
            raise ValueError('Days should be between {} and {} inclusive (got{})'.format(
                self.days_from, self.days_to, days
            ))
        else:
            if self.rent_type == get_codename(rent_rate_types, 'За день'):
                return self.price * days
            else:
                return self.price

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
