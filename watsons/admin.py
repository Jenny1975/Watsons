from django.contrib import admin
from .models import Customer, Transaction, Bonus, Product, Location, Pocket_other, Staff, Servive

# Register your models here.
admin.site.register(Customer)
admin.site.register(Transaction)
admin.site.register(Bonus)
admin.site.register(Location)
admin.site.register(Pocket_other)
admin.site.register(Servive)
admin.site.register(Staff)
class productAdmin(admin.ModelAdmin):
    list_display=('product_id','product_name','category','price','brand','quantity','quantity_safe')
    list_filter=('product_name','category')
    search_fields=('product_name',)
    ordering=('product_id',)
admin.site.register(Product,productAdmin)