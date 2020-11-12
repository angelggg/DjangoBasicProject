from django.contrib import admin
from ciudades.geostats.models import Town, Region, Country


# Register your models here.
class CountryAdmin(admin.ModelAdmin):
    pass


class RegionAdmin(admin.ModelAdmin):
    pass


class TownAdmin(admin.ModelAdmin):
    pass


admin.site.register(Country, CountryAdmin)
admin.site.register(Town, TownAdmin)
admin.site.register(Region, RegionAdmin)
