from django.contrib import admin


from .models import *
# Register your models here.
admin.site.register(CustomUser)

admin.site.register(MilkCenter)
admin.site.register(Customer)
admin.site.register(MilkPurchase)
admin.site.register(MilkSale)
admin.site.register(MakePayment)
admin.site.register(ReceivedPayment)
admin.site.register(Storage)
admin.site.register(Expence)
admin.site.register(CustomerExpence)
admin.site.register(Branch)
admin.site.register(Employee)