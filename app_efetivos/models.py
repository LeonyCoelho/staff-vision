from django.db import models
from django.contrib.auth.models import User

#######################################################################
# AREA ADMINISTRATIVA ============================================================



class Establishment(models.Model):
    establishment_name= models.CharField(max_length=50)
    def __str__(self):
        return self.establishment_name

class Sector(models.Model):
    sector_name = models.CharField(max_length=50)
    def __str__(self):
        return self.sector_name


class Sub_Sector(models.Model):
    subSector_name = models.CharField(max_length=50)
    def __str__(self):
        return self.subSector_name

class Position(models.Model):
    position_name= models.CharField(max_length=50)
    def __str__(self):
        return self.position_name
    
class Shift(models.Model):
    shift_name= models.CharField(max_length=50)
    def __str__(self):
        return self.shift_name

class Theme(models.Model):
    theme_name= models.CharField(max_length=50)
    theme_url= models.CharField(max_length=50, default="default.css")
    def __str__(self):
        return self.theme_name

class Status(models.Model):
    status_name= models.CharField(max_length=50)
    status_color= models.CharField(max_length=50, default="#a5a5a5")
    def __str__(self):
        return self.status_name


class Global_Settings(models.Model):
    establishment_title = models.CharField(max_length=50, default='Estabelecimento')
    sector_title = models.CharField(max_length=50, default='Setor')
    subSector_title = models.CharField(max_length=50, default='Subsetor')
    shift_title = models.CharField(max_length=50, default='Turno')
    position_title = models.CharField(max_length=50, default='Cargo')
    status_title = models.CharField(max_length=50, default='Status')
    theme = models.ManyToManyField(Theme)
    logo_image =  models.ImageField(upload_to='logos/uploaded_logo', default='logos/logo.png')
    bg_image =  models.ImageField(upload_to='bgs/uploaded_bgs', default='bgs/bg.png')
    institution_name = models.CharField(max_length=60, default='Sua Empresa')

class Dashboard_Presets(models.Model):
    preset_name = models.CharField(max_length=50)
    preset_sectors = models.ManyToManyField(Sector)
    
    def __str__(self):
        return self.preset_name
    
class Preset_Settings(models.Model):
    preset = models.ForeignKey(Dashboard_Presets, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    sector_position = models.IntegerField(default=0)
    sector_width = models.IntegerField(default=3)

class Preset_Header(models.Model):
    preset = models.ForeignKey(Dashboard_Presets, on_delete=models.CASCADE)
    header_width = models.IntegerField(default=12)
    
    
class CustomUser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    sector = models.ManyToManyField(Sector)
    preset = models.ManyToManyField(Dashboard_Presets)

    def __str__(self):
        return self.name
    
    def get_username(self):
        return self.user.username

##########################################################################
# WORKERS 

class Worker(models.Model):
    id_worker = models.AutoField(primary_key=True)
    number_w = models.IntegerField(default=0, null=True)
    name_w = models.CharField(max_length=124, null=True)
    position_w =  models.ManyToManyField(Position)
    establishment_w =  models.ManyToManyField(Establishment)
    shift_w =  models.ManyToManyField(Shift)
    sector_w = models.ManyToManyField(Sector)
    subSector_w = models.ManyToManyField(Sub_Sector)
    status_w =  models.ManyToManyField(Status, default="")
    observation_w = models.CharField(max_length=124, default="")

    def __str__(self):
        return str(self.id_worker)