from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^contracts$', contracts, name='contracts'),
    url(r'^contracts/([0-9]+)$', details, name='details'),
    url(r'^contracts/([0-9]+)/gen_contract$', gen_contract, name='gen_contract'),
    url(r'^contracts/([0-9]+)/gen_delivery_act', gen_delivery_act, name='gen_delivery_act'),
    url(r'^contracts/([0-9]+)/gen_return_act', gen_return_act, name='gen_return_act'),
    url(r'^contracts/([0-9]+)/gen_airport', gen_airport, name='gen_airport'),
    url(r'^render', render_docx_set, name='render_docx_set'),
    url(r'^run', run_script, name='run_script'),
    url(r'^get_rate', get_rate, name='get_rate'),
    url(r'^rate_calc', rate_calc, name='rate_calc'),
    url(r'^contracts/new$', new_contract, name='new_contract'),
]
