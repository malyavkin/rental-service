from unittest import TestCase
import requests


class DocxGenTestCase(TestCase):
    def test_render(self):
        api_domain = 'docxtools.dfg.rip'
        api_port = None
        proto = 'https'
        doc_type = 'airport'  # допустимые значения: 'contract','airport','return_act','receive_act'

        if api_port:
            api_url = '{}://{}:{}/render?type={}'.format(proto,
                                                         api_domain,
                                                         api_port,
                                                         doc_type)
        else:
            api_url = '{}://{}/render?type={}'.format(proto,
                                                      api_domain,
                                                      doc_type)

        print(api_url)  # e.g. https://docxtools.dfg.rip/render?type=airport

        r = requests.post(api_url, data={
            'contract_id': 'XX-2016-12-000',
            # все значения переходят в документы так же, как они написаны здесь,
            # никаких преобразований не производится
            'contract_date': '01 Декабря 2016',
            'agent_org': 'Компания',
            'authority_id': '001',
            'authority_date': '01 мая 2016',

            'citizenship': 'Россия',
            'birth_date': '11 ноября 1980',
            'tenant_registration_address': 'Адрес прописки',
            'tenant_residential_address': 'Адрес проживания',
            'tenant_phone_no_contact': '+7 999 1234567',
            'tenant_phone_no_working': '+7 999 9876543',

            # за исключением ФИО -- я автоматически преобразовываю их
            # в формат "Фамилия И. О." для полей, где это надо
            'agent_last_name': 'Агент',
            'agent_first_name': 'Кей',
            'agent_middle_name': 'Смитович',

            'tenant_last_name': 'Фамилия',
            'tenant_first_name': 'Имя',
            'tenant_middle_name': 'Отчество',

            'driver2_last_name': 'Фамилия2',
            'driver2_first_name': 'Имя2',
            'driver2_middle_name': 'Отчество2',

            'driver3_last_name': 'Фамилия3',
            'driver3_first_name': 'Имя3',
            'driver3_middle_name': 'Отчество3',

            'tenant_passport_part': '1234',
            'tenant_passport_number': '567890',
            'tenant_passport_issued': 'ОУФМС Страны по Городу по Району',

            'driver2_passport_part': '1235',
            'driver2_passport_number': '567891',
            'driver2_passport_issued': 'ОУФМС Страны по Городу по Району2',

            'driver3_passport_part': '1236',
            'driver3_passport_number': '567892',
            'driver3_passport_issued': 'ОУФМС Страны по Городу по Району3',

            'tenant_license_no': '1234567890',
            'tenant_license_issued': 'Выдано 1',

            'driver2_license_no': '2468013579',
            'driver2_license_issued': 'Выдано 2',

            'driver3_license_no': '1357924680',
            'driver3_license_issued': 'Выдано 3',

            'car.model': 'Model S',
            'car.vendor': 'Tesla',
            'car.license_no': 'o666oo777',
            'car.PTS': '000PTS000',
            'car.STS': '000STS000',
            'car.VIN': '1234567890987654321',
            'car.year': 2016,
            'car.color': 'Чёрный',
            'car.car_class': 'ABCD',
            'car.OSAGO': '№112233445566778899',
            'car.damages': 'damages',
            'car_current_volume': '0',
            'rent_start_date': '01 декабря 2016',
            'rent_start_time': '15:35',
            'rent_end_date': '01 января 2017',
            'rent_end_time': '00:01',
            'delivery_address': 'адрес выдачи',
            'return_address': 'адрес возврата',
            'area_of_operation': 'Территория эксплутации',
            'booked_class': 'EFGH',
            'tarif': 'тариф',
            'days': '12',
            'total': '1234.56',
            'per_day': '102.88',
            'contract_booking_number': 'booking006',
            'credit_card_no': '5400380012345678',
            'credit_card_valid_until': '05/17',
            'flight_no': 'SU1337',
            'arrive_time': '12:34'
        })

        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.headers['Content-Type'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        self.assertIn('attachment', r.headers['Content-Disposition'])

        with open('download.docx', 'wb') as file:
            file.write(r.content)
