import os
import random
import sys
import django
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sklopime.settings")
django.setup()

from django.contrib.auth.models import User
from app.models import *


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def random_build_price(min_price, max_price):
    return random.randrange(
        min_price,
        max_price,
        500
    )

def create_component(model, **kwargs):
    return model.objects.create(**kwargs)


# -------------------------------------------------
# USERS
# -------------------------------------------------

def create_users():

    users = []

    data = [
        ("cira", "cira@test.com"),
        ("cvetko", "cvetko@test.com"),
        ("coa", "coa@test.com"),
    ]

    for username, email in data:

        user, _ = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email
            }
        )

        user.set_password("Password123")
        user.save()

        profile, _ = UserProfile.objects.get_or_create(
            user=user
        )

        users.append(profile)

    return users


# -------------------------------------------------
# COMPONENTS
# -------------------------------------------------

def create_components():

    components = {}


    # ---------------- CPUs ----------------

    components["ryzen7600"] = Cpu.objects.create(
        name="AMD Ryzen 5 7600",
        description="6 core AM5 gaming processor",
        imagepath="cpu.png",
        powerconsumption=65,
        manufacturer="AMD",
        corecount=6,
        threadcount=12,
        clockspeed=Decimal("3.80"),
        socket="AM5",
        integratedgpu=1
    )


    components["ryzen7800x3d"] = Cpu.objects.create(
        name="AMD Ryzen 7 7800X3D",
        description="High end gaming CPU with 3D cache",
        imagepath="cpu.png",
        powerconsumption=120,
        manufacturer="AMD",
        corecount=8,
        threadcount=16,
        clockspeed=Decimal("4.20"),
        socket="AM5",
        integratedgpu=1
    )


    components["i514600kf"] = Cpu.objects.create(
        name="Intel Core i5-14600KF",
        description="14th generation Intel gaming CPU",
        imagepath="cpu.png",
        powerconsumption=125,
        manufacturer="Intel",
        corecount=14,
        threadcount=20,
        clockspeed=Decimal("3.50"),
        socket="LGA1700",
        integratedgpu=0
    )


    # ---------------- GPUs ----------------

    components["rtx4070"] = Gpu.objects.create(
        name="MSI GeForce RTX 4070 SUPER Ventus 2X",
        description="NVIDIA RTX gaming GPU",
        imagepath="gpu.png",
        powerconsumption=220,
        manufacturer="MSI",
        chip="RTX 4070 SUPER",
        memcapacity="12GB",
        color="Black"
    )


    components["rx7800xt"] = Gpu.objects.create(
        name="Sapphire Radeon RX 7800 XT Pulse",
        description="AMD Radeon gaming GPU",
        imagepath="gpu.png",
        powerconsumption=260,
        manufacturer="Sapphire",
        chip="RX 7800 XT",
        memcapacity="16GB",
        color="Black"
    )


    components["rtx4060"] = Gpu.objects.create(
        name="ASUS Dual RTX 4060",
        description="Budget RTX GPU",
        imagepath="gpu.png",
        powerconsumption=115,
        manufacturer="ASUS",
        chip="RTX 4060",
        memcapacity="8GB",
        color="White"
    )


    # ---------------- RAM ----------------

    components["kingston32"] = Ram.objects.create(
        name="Kingston Fury Beast 32GB DDR5 6000",
        description="DDR5 gaming memory kit",
        imagepath="ram.png",
        powerconsumption=10,
        manufacturer="Kingston",
        type="DDR5",
        speed=6000,
        memcapacity="32GB",
        modulenum=2,
        color="Black"
    )


    components["corsair32"] = Ram.objects.create(
        name="Corsair Vengeance 32GB DDR5 5600",
        description="Corsair DDR5 RAM",
        imagepath="ram.png",
        powerconsumption=10,
        manufacturer="Corsair",
        type="DDR5",
        speed=5600,
        memcapacity="32GB",
        modulenum=2,
        color="Black"
    )


    # ---------------- Motherboards ----------------

    components["msib650"] = Motherboard.objects.create(
        name="MSI MAG B650 Tomahawk WiFi",
        description="AM5 DDR5 motherboard",
        imagepath="mb.png",
        powerconsumption=30,
        manufacturer="MSI",
        socket="AM5",
        formfactor="ATX",
        ramslots=4,
        ramtype="DDR5",
        color="Black",
        wifichip="Intel AX210"
    )


    components["asusb760"] = Motherboard.objects.create(
        name="ASUS TUF Gaming B760-PLUS WiFi",
        description="Intel DDR5 motherboard",
        imagepath="mb.png",
        powerconsumption=35,
        manufacturer="ASUS",
        socket="LGA1700",
        formfactor="ATX",
        ramslots=4,
        ramtype="DDR5",
        color="Black",
        wifichip="Intel WiFi 6"
    )


    # ---------------- Storage ----------------

    components["990pro"] = Storage.objects.create(
        name="Samsung 990 PRO 2TB",
        description="High performance NVMe SSD",
        imagepath="ssd.png",
        powerconsumption=8,
        manufacturer="Samsung",
        type="SSD",
        slot="M.2",
        capacity="2TB"
    )


    components["sn850x"] = Storage.objects.create(
        name="WD Black SN850X 1TB",
        description="Gaming NVMe SSD",
        imagepath="ssd.png",
        powerconsumption=7,
        manufacturer="Western Digital",
        type="SSD",
        slot="M.2",
        capacity="1TB"
    )


    components["barracuda"] = Storage.objects.create(
        name="Seagate Barracuda 2TB",
        description="Desktop HDD",
        imagepath="hdd.png",
        powerconsumption=6,
        manufacturer="Seagate",
        type="HDD",
        slot="SATA",
        capacity="2TB"
    )


    # ---------------- PSU ----------------

    components["rm750"] = Powersupply.objects.create(
        name="Corsair RM750e",
        description="750W Gold PSU",
        imagepath="psu.png",
        powerconsumption=0,
        manufacturer="Corsair",
        formfactor="ATX",
        efficiency="80+ Gold",
        wattage=750
    )


    components["purepower"] = Powersupply.objects.create(
        name="be quiet! Pure Power 12 M 750W",
        description="Silent modular PSU",
        imagepath="psu.png",
        powerconsumption=0,
        manufacturer="be quiet!",
        formfactor="ATX",
        efficiency="80+ Gold",
        wattage=750
    )


    # ---------------- Coolers ----------------

    components["ak400"] = Cpucooler.objects.create(
        name="DeepCool AK400",
        description="Air CPU cooler",
        imagepath="cooler.png",
        powerconsumption=5,
        manufacturer="DeepCool",
        coolertype="Air",
        socket="AM5"
    )


    components["pa120"] = Cpucooler.objects.create(
        name="Thermalright Peerless Assassin 120 SE",
        description="Dual tower air cooler",
        imagepath="cooler.png",
        powerconsumption=7,
        manufacturer="Thermalright",
        coolertype="Air",
        socket="AM5"
    )


    # ---------------- Cases ----------------

    components["nzxt"] = Case.objects.create(
        name="NZXT H5 Flow",
        description="Airflow gaming case",
        imagepath="case.png",
        powerconsumption=0,
        manufacturer="NZXT",
        color="Black",
        dimensions="464x227x446",
        supportedmotherboards="ATX,mATX,ITX"
    )


    components["corsaircase"] = Case.objects.create(
        name="Corsair 4000D Airflow",
        description="Popular airflow case",
        imagepath="case.png",
        powerconsumption=0,
        manufacturer="Corsair",
        color="White",
        dimensions="453x230x466",
        supportedmotherboards="ATX,mATX,ITX"
    )


    return components


# -------------------------------------------------
# BUILDS
# -------------------------------------------------

def add_component_to_build(build, component):
    Buildcomponent.objects.create(
        idbuild=build,
        idcomponent=component
    )


def create_benchmark(build, name, value):
    Benchmark.objects.create(
        idbuild=build,
        name=name,
        value=str(value)
    )


def create_builds(users, components):

    builds = []


    # ---------------- MARKO ----------------

    build = Build.objects.create(
        name="Budget Gaming PC",
        description="Affordable 1080p gaming configuration",
        totalprice=random_build_price(70000, 100000),
        numoflikes=0,
        numofdislikes=0,
        iduser=users[0]
    )

    for c in [
        components["ryzen7600"],
        components["rtx4060"],
        components["kingston32"]
    ]:
        add_component_to_build(build, c)


    create_benchmark(build, "Cinebench R23", 14500)
    create_benchmark(build, "3DMark Time Spy", 11000)

    builds.append(build)



    build = Build.objects.create(
        name="Streaming Beast",
        description="Gaming and streaming setup",
        totalprice=random_build_price(70000, 100000),
        numoflikes=0,
        numofdislikes=0,
        iduser=users[0]
    )

    for c in [
        components["ryzen7800x3d"],
        components["rtx4070"],
        components["990pro"]
    ]:
        add_component_to_build(build, c)


    create_benchmark(build, "Cinebench R23", 18500)
    create_benchmark(build, "3DMark Time Spy", 19500)
    create_benchmark(build, "Geekbench 6", 27000)

    builds.append(build)



    # ---------------- ALEKSA ----------------


    build = Build.objects.create(
        name="AMD Midrange Build",
        description="Balanced gaming computer",
        totalprice=random_build_price(70000, 100000),
        numoflikes=0,
        numofdislikes=0,
        iduser=users[1]
    )

    for c in [
        components["ryzen7600"],
        components["rx7800xt"],
        components["msib650"]
    ]:
        add_component_to_build(build, c)


    create_benchmark(build, "3DMark Time Spy", 17500)
    create_benchmark(build, "Cinebench R23", 15000)

    builds.append(build)



    build = Build.objects.create(
        name="Intel Productivity PC",
        description="Workstation for development and editing",
        totalprice=random_build_price(180000, 260000),
        numoflikes=0,
        numofdislikes=0,
        iduser=users[1]
    )

    for c in [
        components["i514600kf"],
        components["asusb760"],
        components["sn850x"]
    ]:
        add_component_to_build(build, c)


    create_benchmark(build, "Cinebench R23", 22000)
    create_benchmark(build, "Geekbench 6", 25000)

    builds.append(build)



    # ---------------- NIKOLA ----------------


    build = Build.objects.create(
        name="RTX Gaming Machine",
        description="High refresh rate gaming PC",
        totalprice=random_build_price(180000, 260000),
        numoflikes=0,
        numofdislikes=0,
        iduser=users[2]
    )

    for c in [
        components["ryzen7800x3d"],
        components["rtx4070"],
        components["corsair32"]
    ]:
        add_component_to_build(build, c)


    create_benchmark(build, "3DMark Time Spy", 21000)
    create_benchmark(build, "Cinebench R23", 18500)

    builds.append(build)



    build = Build.objects.create(
        name="Silent Office PC",
        description="Quiet computer for everyday work",
        totalprice=random_build_price(180000, 260000),
        numoflikes=0,
        numofdislikes=0,
        iduser=users[2]
    )

    for c in [
        components["ryzen7600"],
        components["990pro"],
        components["purepower"]
    ]:
        add_component_to_build(build, c)


    create_benchmark(build, "Geekbench 6", 22000)

    builds.append(build)


    return builds



# -------------------------------------------------
# LIKES / DISLIKES
# -------------------------------------------------

def create_votes(users, builds):

    votes = [
        (users[0], builds[2], 1),
        (users[0], builds[4], 1),

        (users[1], builds[0], 1),
        (users[1], builds[5], 1),

        (users[2], builds[1], 1),
        (users[2], builds[3], 0),
    ]


    for user, build, like in votes:

        Buildlikedislike.objects.create(
            iduser=user,
            idbuild=build,
            like=like
        )


    # update counters

    for build in builds:

        build.numoflikes = Buildlikedislike.objects.filter(
            idbuild=build,
            like=1
        ).count()

        build.numofdislikes = Buildlikedislike.objects.filter(
            idbuild=build,
            like=0
        ).count()

        build.save()



# -------------------------------------------------
# MAIN
# -------------------------------------------------

def main():

    print("Creating users...")
    users = create_users()


    print("Creating components...")
    components = create_components()


    print("Creating builds...")
    builds = create_builds(
        users,
        components
    )


    print("Creating likes...")
    create_votes(
        users,
        builds
    )


    print("Mock data created successfully!")


if __name__ == "__main__":
    main()