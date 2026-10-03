#Aleksandar Raskovic 2023/0043
from django.contrib import admin

from .models import (
    Benchmark,
    Build,
    Buildcomponent,
    Buildlikedislike,
    Case,
    Component,
    Componentprice,
    Cpu,
    Cpucooler,
    Gpu,
    Motherboard,
    Powersupply,
    Ram,
    Storage,
    UserProfile,
)


@admin.register(Benchmark)
class BenchmarkAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "value", "idbuild")
    search_fields = ("name",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = ("user__username",)


@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ("id", "totalprice", "numoflikes", "numofdislikes", "iduser")


@admin.register(Buildcomponent)
class BuildcomponentAdmin(admin.ModelAdmin):
    list_display = ("id", "idcomponent", "idbuild")


@admin.register(Buildlikedislike)
class BuildlikedislikeAdmin(admin.ModelAdmin):
    list_display = ("id", "like", "iduser", "idbuild")


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "imagepath", "powerconsumption", "manufacturer")
    search_fields = ("name",)


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "imagepath", "powerconsumption", "manufacturer", "color", "dimensions", "supportedmotherboards")
    search_fields = ("name",)


@admin.register(Componentprice)
class ComponentpriceAdmin(admin.ModelAdmin):
    list_display = ("id", "shopname", "link", "price", "idcomponent", "idcomponent__name")


@admin.register(Cpu)
class CpuAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "imagepath", "powerconsumption", "manufacturer", "corecount", "threadcount", "clockspeed", "socket", "integratedgpu")
    search_fields = ("name",)


@admin.register(Cpucooler)
class CpucoolerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "imagepath", "powerconsumption", "manufacturer", "coolertype", "socket")
    search_fields = ("name",)


@admin.register(Gpu)
class GpuAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "imagepath", "powerconsumption", "manufacturer", "chip", "memcapacity", "color")
    search_fields = ("name",)


@admin.register(Motherboard)
class MotherboardAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "imagepath", "powerconsumption", "manufacturer", "socket", "formfactor", "ramslots", "ramtype", "color", "wifichip")
    search_fields = ("name",)


@admin.register(Powersupply)
class PowersupplyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "imagepath", "powerconsumption", "manufacturer", "formfactor", "efficiency", "wattage")
    search_fields = ("name",)


@admin.register(Ram)
class RamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "imagepath", "powerconsumption", "manufacturer", "type", "speed", "memcapacity", "modulenum", "color")
    search_fields = ("name",)


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "imagepath", "powerconsumption", "manufacturer", "type", "slot", "capacity")
    search_fields = ("name",)
