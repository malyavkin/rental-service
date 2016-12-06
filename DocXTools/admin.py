from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Car)
admin.site.register(Address)
admin.site.register(Representative)
admin.site.register(Contract)
admin.site.register(Company)
admin.site.register(CarClass)
admin.site.register(DocXTemplate)
admin.site.register(DocXDocument)
admin.site.register(Rate)
admin.site.register(Branch)
