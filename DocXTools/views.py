import json
import os
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from sendfile import sendfile

from DocXTools.forms import CalcForm, ContractForm
from DocXTools.internals import create_contract_from_form, query_rates, serve_doc, render_docx
from DocXTools.models import Address, Branch, CarClass, Contract, DocXTemplate
from DocXTools.templates.formats import iso8601_date

TIMES = ['{:0>2}:{:0>2}'.format(h, m) for h in range(24) for m in [0, 30]]


class HomeView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return render(request, 'index.html')


@login_required
def contracts(request):
    ctx = {'contracts': Contract.objects.all()}
    return render(request, 'contracts.html', ctx)


@login_required
def details(request, contract_id):
    contract = Contract.objects.get(pk=int(contract_id))
    ctx = {
        'contract':  contract,
        'names':     [contract.get_driver_fio(i) for i in [1, 2, 3]],
        'passports': [contract.get_driver_passport(i) for i in [1, 2, 3]],
        'licenses':  [contract.get_driver_license(i) for i in [1, 2, 3]]
    }
    return render(request, 'details.html', ctx)


@login_required
def new_contract(request):
    now = datetime.now()
    default_name = now.strftime('%Y_%m')
    now_str = now.strftime(iso8601_date)
    delivery_addresses = Address.objects.all()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = create_contract_from_form(request, form)
            return redirect('details', contract.pk)
        else:
            print('form is invalid')

    else:

        form = ContractForm(initial={
            'contract_date':   now_str,
            'rent_start_date': now_str,
            'rent_end_date':   now_str,
            'birth_date':      now_str
        })

    return render(request, 'new_form.html', {'form':               form,
                                             'delivery_addresses': delivery_addresses,
                                             'times':              TIMES,
                                             'default_name':       default_name})


@login_required
def gen_contract(request, contract_id):
    contract = Contract.objects.get(pk=contract_id)
    return serve_doc(contract, 'договор', request)


@login_required
def gen_delivery_act(request, contract_id):
    contract = Contract.objects.get(pk=contract_id)
    return serve_doc(contract, 'акт_выдачи', request)


@login_required
def gen_return_act(request, contract_id):
    contract = Contract.objects.get(pk=contract_id)
    return serve_doc(contract, 'акт_возврата', request)


@login_required
def gen_airport(request, contract_id):
    contract = Contract.objects.get(pk=contract_id)
    return serve_doc(contract, 'табличка', request)


@login_required
def run_script(request):
    from DocXTools.rates.init_rates import init_rates
    init_rates()
    return HttpResponse('ok')


@login_required
def rate_calc(request):
    data = {}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CalcForm(request.POST)
        if form.is_valid():
            data = query_rates(booking_date=form.cleaned_data['booking_date'],
                               days=form.cleaned_data['days'],
                               branch=form.cleaned_data['branch'],
                               car_class=form.cleaned_data['car_class'],
                               citizenship=form.cleaned_data['citizenship'])
        else:
            print('form is invalid')

    else:
        form = CalcForm()

    if 'rates' in data:
        for rate in data['rates']:
            rate['json'] = json.dumps(rate['json'], ensure_ascii=False, indent=4, sort_keys=True)

    ctx = {
        'form': form,
        'data': data
    }

    return render(request, 'rate_calc.html', ctx)


@login_required
def get_rate(request):
    # sample: /get_rate?booking_date=2017-01-02&car_class=EDAR&days=7&branch=Симферополь&citizenship=rus
    booking_date_raw = request.GET['booking_date']
    car_class = request.GET['car_class']
    days = int(request.GET['days'])
    branch_name = request.GET['branch']
    citizenship = request.GET['citizenship']
    booking_date = datetime.strptime(booking_date_raw, iso8601_date).date()
    ctx = query_rates(booking_date=booking_date,
                      days=days,
                      branch=Branch.objects.get(name=branch_name),
                      car_class=CarClass.objects.get(class_namr=car_class),
                      citizenship=citizenship)
    return JsonResponse(ctx, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def render_docx_set(request):
    alias = {'contract': 'договор',
             'airport': 'табличка',
             'return_act': 'акт_возврата',
             'receive_act': 'акт_выдачи'}
    tpl_name = alias[request.GET['type']]
    template = DocXTemplate.objects.get(template_name=tpl_name)
    post = request.POST
    path = 'DocXTools/media/tmp.docx'
    try:
        os.remove(path)
    except FileNotFoundError as x:
        pass

    pass_tpl = '№{} {}; выдан {}'
    dr_lic_tpl = '№{}; выдано {}'
    ctx = {k:v for k,v in post.items()}
    ctx.update({
        'agent_fio': ' '.join([
            post['agent_last_name'],
            post['agent_first_name'],
            post['agent_middle_name'],
        ]),
        'names': [
            ' '.join([
                post['tenant_last_name'],
                post['tenant_first_name'],
                post['tenant_middle_name'],
            ]),
            ' '.join([
                post['driver2_last_name'],
                post['driver2_first_name'],
                post['driver2_middle_name'],
            ]),
            ' '.join([
                post['driver3_last_name'],
                post['driver3_first_name'],
                post['driver3_middle_name'],
            ]),
        ],
        'passports': [
            pass_tpl.format(
                post['tenant_passport_part'],
                post['tenant_passport_number'],
                post['tenant_passport_issued'],
            ),
            pass_tpl.format(
                post['driver2_passport_part'],
                post['driver2_passport_number'],
                post['driver2_passport_issued'],
            ),
            pass_tpl.format(
                post['driver3_passport_part'],
                post['driver3_passport_number'],
                post['driver3_passport_issued'],
            ),

        ],
        'licenses': [
            dr_lic_tpl.format(
                post['tenant_license_no'],
                post['tenant_license_issued'],
            ),
            dr_lic_tpl.format(
                post['driver2_license_no'],
                post['driver2_license_issued'],
            ),
            dr_lic_tpl.format(
                post['driver3_license_no'],
                post['driver3_license_issued'],
            )
        ],
    })

    ctx['car'] = {k[4:]: v for k,v in post.items() if k[:4] == 'car.'}
    ctx['car']['car_class'] = {'class_name': ctx['car']['car_class']}
    ctx['rub'] = ctx['total'][:-3]
    ctx['kop'] = ctx['total'][-2:]
    ctx['agent_title'] = '{} {}. {}.'.format(
        post['agent_last_name'],
        post['agent_first_name'][:1],
        post['agent_middle_name'][:1]
    )
    ctx['tenant_title'] = '{} {}. {}.'.format(
        post['tenant_last_name'],
        post['tenant_first_name'][:1],
        post['tenant_middle_name'][:1]
    )

    print(json.dumps(ctx, indent=4,sort_keys=True, ensure_ascii=False))
    render_docx(template, ctx, path)
    return sendfile(request, path, attachment=True)