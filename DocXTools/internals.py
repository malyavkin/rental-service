import os

from django.conf import settings
from django.db.models import Q
from docxtpl import DocxTemplate
from sendfile import sendfile

from DocXTools.models import Contract, DocXDocument, DocXTemplate, Rate


# todo: сделать это всё ModelForm и перегрузить save()
def create_contract_from_form(request, form):
    map_form_to_model = [
        'contract_date',
        'contract_booking_number',
        'car',
        'booked_class',
        'delivery_address',
        'area_of_operation',
        'return_address',
        'flight_no',
        'arrive_time',
        'tenant_first_name',
        'tenant_middle_name',
        'tenant_last_name',
        'tenant_passport_part',
        'tenant_passport_number',
        'tenant_passport_issued',
        'tenant_phone_no_contact',
        'tenant_phone_no_working',
        'email',
        'tenant_driver_license_no',
        'tenant_driver_license_issued',
        'citizenship',
        'birth_date',
        'tenant_registration_address',
        'tenant_residential_address',
        'rent_start_date',
        'rent_start_time',
        'rent_end_date',
        'rent_end_time',

        'driver2_first_name',
        'driver2_middle_name',
        'driver2_last_name',
        'driver2_passport_part',
        'driver2_passport_number',
        'driver2_passport_issued',
        'driver2_driver_license_no',
        'driver2_driver_license_issued',
        'driver2_registration_address',
        'driver2_phone_no_contact',

        'driver3_first_name',
        'driver3_middle_name',
        'driver3_last_name',
        'driver3_passport_part',
        'driver3_passport_number',
        'driver3_passport_issued',
        'driver3_driver_license_no',
        'driver3_driver_license_issued',
        'driver3_registration_address',
        'driver3_phone_no_contact',
        'car_current_volume',
    ]
    contract = Contract()
    for field in map_form_to_model:
        setattr(contract, field, form.cleaned_data[field])

    if request.user.representative:
        contract.agent = request.user.representative

    contract.save()
    # create docs
    for template in DocXTemplate.objects.all():
        create_docx(contract, template)

    return contract


def create_docx(contract, template):
    f = Contract._meta.get_fields()
    ctx = {k.name: getattr(contract, k.name, None) for k in f}
    agent = contract.get_agent_state()
    car = contract.get_car_state()
    ctx.update({
        'contract_id':               contract.get_complete_number(),
        'agent_org': agent['company']['org_name'],
        'agent_fio':                 "{} {} {}".format(agent['user']['last_name'],
                                                       agent['user']['first_name'],
                                                       agent['middle_name']),
        'authority_id':              agent['company_authority_id'],
        'authority_date':            agent['issue_date'],
        'car':                       car,
        'booked_class':              contract.booked_class.class_name,
        'agent_title':               "{} {}. {}.".format(agent['user']['last_name'],
                                                         agent['user']['first_name'][:1],
                                                         agent['middle_name'][:1]),
        'tenant_title':              "{} {}. {}.".format(contract.tenant_last_name,
                                                         contract.tenant_first_name[:1],
                                                         contract.tenant_middle_name[:1]),
        'names':                     [contract.get_driver_fio(i) for i in [1, 2, 3]],
        'passports':                 [contract.get_driver_passport(i) for i in [1, 2, 3]],
        'licenses':                  [contract.get_driver_license(i) for i in [1, 2, 3]]
    })
    media_root = getattr(settings, 'SENDFILE_ROOT', None)
    name = "{}_{}.docx".format(contract.get_complete_number(), template.template_name)
    path = os.path.join(media_root, name)
    render_docx(template, ctx, path)

    document = DocXDocument()
    document.contract = contract
    document.template = template
    document.path = path
    document.save()


def render_docx(template, ctx, path):
    docx_root = getattr(settings, 'DOCX_TEMPLATES_ROOT', None)
    doc = DocxTemplate(os.path.join(docx_root, template.template_path))
    try:
        doc.render(ctx)
        doc.save(path)
    except Exception as x:
        print(x)


def serve_doc(contract, template_name, request):
    template = DocXTemplate.objects.get(template_name=template_name)
    doc = DocXDocument.objects.get(template=template, contract=contract)
    return sendfile(request, doc.path, attachment=True)


def query_rates(booking_date=None, days=None, branch=None, car_class=None, citizenship=None):
    rates = Rate.objects.filter(
        booking_from__lte=booking_date,
        booking_to__gt=booking_date,
        car_class=car_class,
        branch=branch,
        days_from__lte=days,
        days_to__gte=days
    ).filter(
        Q(citizenship=citizenship) | Q(citizenship='*')
    )
    # Тут у нас все возможные тарифы по заданным критериям
    # В случае, если среди них есть тарифы для запрошенного гражданства, выбрать только их, иначе
    # вернуть все
    rates_for_citizenship = [rate for rate in rates if rate.citizenship == citizenship]
    if len(rates_for_citizenship):
        rates = rates_for_citizenship

    ctx = {
        'rates': [{
            'total': rate.get_total_for_days(days),
            'price': rate.price,
            'cur':   rate.currency,
            'json':  rate.get_json()
        } for rate in rates]
    }

    return ctx
