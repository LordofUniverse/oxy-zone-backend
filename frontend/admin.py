from django.contrib import admin
from .models import Sellers, Places

class SellersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'password', 'profilephoto')

class PlacesAdmin(admin.ModelAdmin):
    list_display = ('foreign_seller', 'location', 'addr', 'phno', 'oxyprice')

# Register your models here.

admin.site.register(Sellers, SellersAdmin)
admin.site.register(Places, PlacesAdmin)
