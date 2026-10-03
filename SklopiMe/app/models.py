#Aleksandar Cvetkovic 2023/0150
#Aleksandar Raskovic 2023/0043 - izmenjao user na djangov i napravio da se koristi inheritance
#Marko Ciric 2023/0133 - SSU6/7/8: dodati name, description u Build, Buildimage tabela

from django.contrib.auth.models import User
from django.db import models



class Benchmark(models.Model):
    """
    Benchmark rezultati za build.
    
    Čuva benchmark vrednosti vezane uz specifičan build (FPS, procesorski score, itd.)
    """
    name = models.CharField(max_length=45)
    value = models.CharField(max_length=45)
    idbuild = models.ForeignKey('Build', models.CASCADE, db_column='idBuild', related_name='benchmarks')

    class Meta:
        db_table = 'benchmark'

class UserProfile(models.Model):
    """
    Profil korisnika.
    
    Proširenje Django User modela sa dodatnim korisničkim informacijama.
    Svaki korisnik ima jedan profil.
    """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.user.username

class Build(models.Model):
    """
    Gotov računar.
    
    Predstavlja objavljenu ili spremljenu računarsku konfiguraciju od strane korisnika.
    Sadrži ukupnu cenu, opis, i broj lajkova/dislajkova.
    """
    name = models.CharField(max_length=100, default='My build')
    description = models.TextField(blank=True, null=True)
    totalprice = models.IntegerField(db_column='totalPrice')
    numoflikes = models.IntegerField(db_column='numOfLikes')  
    numofdislikes = models.IntegerField(db_column='numOfDislikes')  
    iduser = models.ForeignKey(UserProfile, models.CASCADE, db_column='idUser')

    class Meta:
        db_table = 'build'

    def __str__(self):
        return self.name


class Buildcomponent(models.Model):
    """
    Veza između build-a i komponenti.
    
    Many-to-many povezivanje između build konfiguracije i računarskih komponenti.
    Omogućava build-u da sadrži više različitih komponenti.
    """
    idcomponent = models.ForeignKey('Component', models.CASCADE, db_column='idComponent')
    idbuild = models.ForeignKey(Build, models.CASCADE, db_column='idBuild')

    class Meta:
        db_table = 'buildcomponent'


class Buildimage(models.Model):
    """
    Slike build konfiguracije.
    
    Čuva slike prikupljene iz interneta ili upload-ovane od strane korisnika
    koje su povezane sa specifičnim build-om.
    """
    idbuild = models.ForeignKey(Build, models.CASCADE, db_column='idBuild', related_name='images')
    image = models.ImageField(upload_to='app/static/build_images')

    class Meta:
        db_table = 'buildimage'


class Buildlikedislike(models.Model):
    """
    Lajkovi i dislajkovi na build.
    
    Čuva glas (lajk ili dislajk) od strane korisnika na specifičan build.
    Korisniku je dozvoljeno da ima samo jedan glas po build-u.
    """
    like = models.IntegerField()
    iduser = models.ForeignKey(UserProfile, models.CASCADE, db_column='idUser')
    idbuild = models.ForeignKey(Build, models.CASCADE, db_column='idBuild')

    class Meta:
        db_table = 'buildlikedislike'


class Component(models.Model):
    """
    Bazna klasa za sve računarske komponente.
    
    Koristi model nasleđivanja (inheritance) u Django-u. Sadrži opšte informacije
    koje se primenjuju na sve komponente (naziv, proizvodač, potrošnja struje, itd.).
    Specifične komponente (CPU, GPU, RAM, itd.) nasleđuju ovu klasu.
    """
    name = models.CharField(max_length=45,unique=True)
    description = models.CharField(max_length=255)
    imagepath = models.CharField(db_column='imagePath', max_length=255)
    powerconsumption = models.IntegerField(db_column='powerConsumption')  
    manufacturer = models.CharField(max_length=45)

    class Meta:
        db_table = 'component'

    def __str__(self):
        return self.name


class Case(Component):
    """
    Kućište za računar.
    
    Predstavlja fizičko kućište u koje se stavljaju sve druge komponente.
    Nasleđuje Component klasu i dodaje specifična svojstva kućišta.
    """
    component_ptr = models.OneToOneField(Component, models.CASCADE, db_column='id', parent_link=True, primary_key=True)
    color = models.CharField(max_length=45)
    dimensions = models.CharField(max_length=45)
    supportedmotherboards = models.CharField(db_column='supportedMotherboards', max_length=45)  

    class Meta:
        db_table = 'case'


class Componentprice(models.Model):
    """
    Cena komponente kod određene prodavnice.
    
    Povezuje komponente sa njihovim cenama i linkovima iz različitih online prodavnica.
    Ista komponenta može imati više cena iz različitih prodavnica.
    """
    shopname = models.CharField(db_column='shopName', max_length=45)
    link = models.CharField(max_length=255)
    price = models.IntegerField()
    idcomponent = models.ForeignKey(Component, models.CASCADE, db_column='idComponent')

    class Meta:
        db_table = 'componentprice'


class Cpu(Component):
    """
    Procesor (CPU).
    
    Predstavlja procesore sa specifičnim svojstvima kao broj jezgara, frekvencija,
    tip soketa i integrirana grafika. Nasleđuje Component klasu.
    """
    component_ptr = models.OneToOneField(Component, models.CASCADE, db_column='id', parent_link=True, primary_key=True)
    corecount = models.IntegerField(db_column='coreCount')  
    threadcount = models.IntegerField(db_column='threadCount')  
    clockspeed = models.DecimalField(max_digits = 4,decimal_places=2,db_column='clockSpeed')  
    socket = models.CharField(max_length=45)
    integratedgpu = models.IntegerField(db_column='integratedGPU')  

    class Meta:
        db_table = 'cpu'


class Cpucooler(Component):
    """
    Hladnjak za procesor.
    
    Predstavlja hladnjak za CPU sa svojstvima kao tip hlađenja (vazdušno ili tečno)
    i kompatibilni soketi. Nasleđuje Component klasu.
    """
    component_ptr = models.OneToOneField(Component, models.CASCADE, db_column='id', parent_link=True, primary_key=True)
    coolertype = models.CharField(db_column='coolerType', max_length=5)  
    socket = models.CharField(max_length=45)

    class Meta:
        db_table = 'cpucooler'


class Gpu(Component):
    """
    Grafička kartica (GPU).
    
    Predstavlja grafičke kartice sa svojstvima kao čip, kapacitet memorije i boja.
    Nasleđuje Component klasu.
    """
    component_ptr = models.OneToOneField(Component, models.CASCADE, db_column='id', parent_link=True, primary_key=True)
    chip = models.CharField(max_length=45)
    memcapacity = models.CharField(db_column='memCapacity', max_length=10)  
    color = models.CharField(max_length=45)

    class Meta:
        db_table = 'gpu'


class Motherboard(Component):
    """
    Matična ploča (Motherboard).
    
    Predstavlja matične ploče sa svojstvima kao tip soketa, faktor forma,
    broj RAM slotova, tip RAM-a i WiFi čip. Nasleđuje Component klasu.
    """
    component_ptr = models.OneToOneField(Component, models.CASCADE, db_column='id', parent_link=True, primary_key=True)
    socket = models.CharField(max_length=45)
    formfactor = models.CharField(db_column='formFactor', max_length=45)  
    ramslots = models.IntegerField(db_column='ramSlots')  
    ramtype = models.CharField(db_column='ramType', max_length=20)  
    color = models.CharField(max_length=45)
    wifichip = models.CharField(db_column='wifiChip', max_length=45)  

    class Meta:
        db_table = 'motherboard'


class Powersupply(Component):
    """
    Napajanje (Power Supply Unit).
    
    Predstavlja napajanja sa svojstvima kao faktor forma, efikasnost i snaga u vat.
    Nasleđuje Component klasu.
    """
    component_ptr = models.OneToOneField(Component, models.CASCADE, db_column='id', parent_link=True, primary_key=True)
    formfactor = models.CharField(db_column='formFactor', max_length=45)  
    efficiency = models.CharField(max_length=45)
    wattage = models.IntegerField()

    class Meta:
        db_table = 'powersupply'


class Ram(Component):
    """
    RAM memorija (Random Access Memory).
    
    Predstavlja RAM memoriju sa svojstvima kao tip, brzina, kapacitet i broj modula.
    Nasleđuje Component klasu.
    """
    component_ptr = models.OneToOneField(Component, models.CASCADE, db_column='id', parent_link=True, primary_key=True)
    type = models.CharField(max_length=45)
    speed = models.IntegerField()
    memcapacity = models.CharField(db_column='memCapacity', max_length=10)  
    modulenum = models.IntegerField(db_column='moduleNum')  
    color = models.CharField(max_length=45)

    class Meta:
        db_table = 'ram'


class Storage(Component):
    """
    Memorijski disk (HDD, SSD, NVME).
    
    Predstavlja memorijske uređaje sa svojstvima kao tip (HDD, SSD, NVME),
    slot (M.2, SATA, itd.) i kapacitet. Nasleđuje Component klasu.
    """
    component_ptr = models.OneToOneField(Component, models.CASCADE, db_column='id', parent_link=True, primary_key=True)
    type = models.CharField(max_length=3)
    slot = models.CharField(max_length=45)
    capacity = models.CharField(max_length=10)

    class Meta:
        db_table = 'storage'